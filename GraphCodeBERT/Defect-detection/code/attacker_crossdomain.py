import sys
import os

sys.path.append('../../../')
sys.path.append('../../../python_parser')

import csv
import copy
import json
import logging
import argparse
import warnings
import re
import torch
import math
import torch.nn as nn
import numpy as np
import random
from run import InputFeatures
from utils import select_parents, crossover, map_chromesome, mutate, is_valid_variable_name, _tokenize, get_identifier_posistions_from_code, get_masked_code_by_position, get_substitutes, is_valid_substitute, set_seed

from utils import GraphCodeDataset
from utils import getUID, isUID, getTensor, build_vocab
from run_parser import get_identifiers, get_example, extract_dataflow

class CrossDomainAttacker():
    def __init__(self, args, model_sub, model_tgt, tokenizer, model_mlm, tokenizer_mlm, targeted=False) -> None:
        self.args = args
        self.model_sub = model_sub                        # substitute model (input: token_ids, output: embeddings)
        self.model_tgt = model_tgt                        # target model (input: tokens_ids, output: classify_logits)
        self.tokenizer = tokenizer                        # tokenizer of the substitute & target model
        self.model_mlm = model_mlm                        # no use here
        self.tokenizer_mlm = tokenizer_mlm                # used to convert the words into lowercase       
        self.iterations = 1
        self.targeted = targeted
    

    def loss(self, embedding_a, embedding_b):
        '''
        compute the squared distance between embedding_a and embedding_b
        '''        
        return nn.MSELoss()(embedding_a.to(self.args.device), embedding_b.to(self.args.device)).item()

    
    # def compute_fitness(self, chromesome, codebert_tgt, tokenizer_tgt, orig_prob, orig_label, true_label ,code, names_positions_dict, args, orig_example=None, target_example=None):
    #     # 计算fitness function.
    #     # words + chromesome + orig_label + current_prob
    #     temp_code = map_chromesome(chromesome, code, "c")
    #     new_feature = self.convert_code_to_features(temp_code).input_ids
    #     new_embeddings = self.model_sub(torch.tensor(new_feature).unsqueeze(0).to(self.args.device))[0]
    #     if target_example is not None:
    #         target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
    #         fitness_value = -self.loss(target_embeddings, new_embeddings)
    #     else:
    #         orig_embeddings = self.model_sub(orig_example[0].unsqueeze(0).to(self.args.device))[0]
    #         fitness_value = self.loss(orig_embeddings, new_embeddings)
    #     return fitness_value

    def features_to_model_sub(self, InputFeatures, args):
        input_ids = InputFeatures.input_ids
        position_idx = InputFeatures.position_idx
        dfg_to_code = InputFeatures.dfg_to_code
        dfg_to_dfg = InputFeatures.dfg_to_dfg

        #calculate graph-guided masked function
        attn_mask=np.zeros((args.code_length+args.data_flow_length,
                            args.code_length+args.data_flow_length),dtype=np.bool)
        #calculate begin index of node and max length of input
        
        node_index=sum([i>1 for i in position_idx])
        max_length=sum([i!=1 for i in position_idx])
        #sequence can attend to sequence
        attn_mask[:node_index,:node_index]=True
        #special tokens attend to all tokens
        for idx,i in enumerate(input_ids):
            if i in [0,2]:
                attn_mask[idx,:max_length]=True
        #nodes attend to code tokens that are identified from
        for idx,(a,b) in enumerate(dfg_to_code):
            if a<node_index and b<node_index:
                attn_mask[idx+node_index,a:b]=True
                attn_mask[a:b,idx+node_index]=True
        #nodes attend to adjacent nodes 
        for idx,nodes in enumerate(dfg_to_dfg):
            for a in nodes:
                if a+node_index<len(position_idx):
                    attn_mask[idx+node_index,a+node_index]=True
        
        return input_ids, attn_mask, position_idx

    def convert_code_to_features(self, code, tokenizer, label, args):
        # 这里要被修改..
        code=' '.join(code.split())
        dfg, index_table, code_tokens = extract_dataflow(code, "c")
        code_tokens=[tokenizer.tokenize('@ '+x)[1:] if idx!=0 else tokenizer.tokenize(x) for idx,x in enumerate(code_tokens)]
        ori2cur_pos={}
        ori2cur_pos[-1]=(0,0)
        for i in range(len(code_tokens)):
            ori2cur_pos[i]=(ori2cur_pos[i-1][1],ori2cur_pos[i-1][1]+len(code_tokens[i]))    
        code_tokens=[y for x in code_tokens for y in x]

        code_tokens=code_tokens[:args.code_length+args.data_flow_length-2-min(len(dfg),args.data_flow_length)]
        source_tokens =[tokenizer.cls_token]+code_tokens+[tokenizer.sep_token]
        source_ids =  tokenizer.convert_tokens_to_ids(source_tokens)
        position_idx = [i+tokenizer.pad_token_id + 1 for i in range(len(source_tokens))]
        dfg = dfg[:args.code_length+args.data_flow_length-len(source_tokens)]
        source_tokens += [x[0] for x in dfg]
        position_idx+=[0 for x in dfg]
        source_ids+=[tokenizer.unk_token_id for x in dfg]
        padding_length=args.code_length+args.data_flow_length-len(source_ids)
        position_idx+=[tokenizer.pad_token_id]*padding_length
        source_ids+=[tokenizer.pad_token_id]*padding_length

        reverse_index={}
        for idx,x in enumerate(dfg):
            reverse_index[x[1]]=idx
        for idx,x in enumerate(dfg):
            dfg[idx]=x[:-1]+([reverse_index[i] for i in x[-1] if i in reverse_index],)    
        dfg_to_dfg=[x[-1] for x in dfg]
        dfg_to_code=[ori2cur_pos[x[1]] for x in dfg]
        length=len([tokenizer.cls_token])
        dfg_to_code=[(x[0]+length,x[1]+length) for x in dfg_to_code]
        
        return InputFeatures(source_tokens, source_ids, position_idx, dfg_to_code, dfg_to_dfg, 0, label)


    def get_importance_score(self, example, code, words_list: list, sub_words: list, variable_names: list, model_type='classification', target_example=None):
        '''
        Compute the importance score of each variable. Replace each variable to see its influence on the output confidence
        '''
        # label: example[1] tensor(1)
        # 1. 过滤掉所有的keywords.
        positions = get_identifier_posistions_from_code(words_list, variable_names)
        # 需要注意大小写.
        if len(positions) == 0:
            ## 没有提取出可以mutate的position
            print('Error! (in get_importance_score) len(positions)==0')
            return None, None, None

        new_examples = []

        # 2. 得到Masked_tokens, whose length equals to the number of the manipulated code
        masked_token_list, replace_token_positions = get_masked_code_by_position(words_list, positions)
        # replace_token_positions 表示着，哪一个位置的token被替换了.

        for index, tokens in enumerate([words_list] + masked_token_list):
            # words_list denotes the original code?
            new_code = ' '.join(tokens)
            new_feature = self.convert_code_to_features(new_code, self.tokenizer, example[3].item(), self.args)
            new_examples.append(new_feature)
        # 3. 将他们转化成features
        embeddings_list = []
        for feature in new_examples:
            # detach here is necessary to aviod OOM
            input_ids, attn_mask, position_idx = self.features_to_model_sub(feature, self.args)
            embeddings_list.append(self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu())   
        embeddings = torch.stack(embeddings_list)


        if self.targeted:
            target_embeddings = self.model_sub(torch.tensor(target_example[0]).unsqueeze(0).to(self.args.device))[0]

        orig_embeddings = embeddings[0]
        importance_score = []
        for embed in embeddings[1:]:
            if self.targeted:
                importance_score.append(self.loss(orig_embeddings, target_embeddings) - self.loss(embed, target_embeddings))
            else:
                importance_score.append(self.loss(embed, orig_embeddings))

        return importance_score, replace_token_positions, positions


    def get_importance_score_explain(self, args, example, code, words_list: list, sub_words: list, variable_names: list, tgt_model, tokenizer, label_list, batch_size=16, max_length=512, model_type='classification'):
        '''Compute the importance score of each variable'''
        # label: example[1] tensor(1)
        # 1. 过滤掉所有的keywords.
        positions = get_identifier_posistions_from_code(words_list, variable_names)
        # 需要注意大小写.
        if len(positions) == 0:
            ## 没有提取出可以mutate的position
            return None, None, None

        new_example = []

        # 2. 得到Masked_tokens
        masked_token_list, replace_token_positions = get_masked_code_by_position(words_list, positions)
        # replace_token_positions 表示着，哪一个位置的token被替换了.


        for index, tokens in enumerate([words_list] + masked_token_list):
            new_code = ' '.join(tokens)
            new_feature = self.convert_code_to_features(new_code, tokenizer, example[3].item(), args)
            new_example.append(new_feature)
        new_dataset = GraphCodeDataset(new_example, args)
        # 3. 将他们转化成features
        logits, preds = tgt_model.get_results(new_dataset, args.eval_batch_size)
        orig_probs = logits[0]
        orig_label = preds[0]
        # 第一个是original code的数据.
        
        orig_prob = max(orig_probs)
        # predicted label对应的probability

        importance_score = []
        for prob in logits[1:]:
            importance_score.append(abs(orig_prob - prob[orig_label]))

        return importance_score, replace_token_positions, positions

    def variable_influence_value(self, example, code, subs):
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[3].item()

        identifiers, code_tokens = get_identifiers(code, 'c')
        prog_length = len(code_tokens)
        processed_code = " ".join(code_tokens)
        
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            return None
            
        if len(variable_names) == 0:
            # 没有提取到identifier，直接退出
            print('Error! No variable_names extracted!')
            return None

        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.code_length - 2] + [self.tokenizer.sep_token]
        
        # 计算importance_score.
        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score_explain(self.args, example, 
                                                processed_code,
                                                words,
                                                sub_words,
                                                variable_names,
                                                self.model_tgt, 
                                                self.tokenizer, 
                                                [0,1], 
                                                batch_size=self.args.eval_batch_size, 
                                                max_length=self.args.code_length, 
                                                model_type='classification')

        if importance_score is None:
            print('Error! Importance_score is None!')
            return None

        return np.mean(importance_score)
    

    def greedy_attack(self, example, code, subs, target_example=None):
        '''
        return
            original program: code
            program length: prog_length
            adversar program: adv_program
            true label: true_label
            original prediction: orig_label
            adversarial prediction: temp_label
            is_attack_success: is_success
            extracted variables: variable_names
            importance score of variables: names_to_importance_score
            number of changed variables: nb_changed_var
            number of changed positions: nb_changed_pos
            substitutes for variables: replaced_words
        '''
            # 先得到tgt_model针对原始Example的预测信息.

        # for k, _ in subs.items():
        #     subs[k].remove('flat')
        # print('removed flat from subs!')

        logits, preds = self.model_tgt.get_results([example], 1)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[3].item()
        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device), example[1].unsqueeze(0).to(self.args.device), example[2].unsqueeze(0).to(self.args.device))[0]

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0


        # random initialization the adv_code
        replaced_words = {}
        identifiers, code_tokens = get_identifiers(adv_code, 'c') 
        # print('identifiers: {}, subs.keys(): {}'.format(identifiers, subs.keys()))  # test
        used_substitutes = []
        for tgt_word in identifiers:
            tgt_word = tgt_word[0]
            if tgt_word not in subs.keys():
                continue
            all_substitutes = subs[tgt_word]
            for item in used_substitutes:
                if item in all_substitutes:
                    all_substitutes.remove(item)
            substitute = random.choice(all_substitutes)
            replaced_words[tgt_word] = substitute
            subs[substitute] = all_substitutes
            used_substitutes.append(substitute)
            adv_code = get_example(adv_code, tgt_word, substitute, 'c')
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        identifiers, code_tokens = get_identifiers(adv_code, 'c') 
        prog_length = len(code_tokens)

        processed_code = " ".join(code_tokens)
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)

        variable_names = list(subs.keys())  # a list of all variables, including un-identifiers and identifiers
        
        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None
            
        if len(variable_names) == 0:
            # 没有提取到identifier，直接退出
            is_success = -3
            temp_label = orig_label
            print('Error! No variable_names extracted!')
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.code_length - 2] + [self.tokenizer.sep_token]

        # 计算importance_score.

        # name_positions_dict: {key: identifier, value: a list records all the positions that the identifier occurs}
        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score(
                                                example,
                                                processed_code,
                                                words,
                                                sub_words,
                                                variable_names,
                                                target_example=target_example,)

        if importance_score is None:
            print('Error! Importance_score is None!')
            temp_label = true_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, -3, variable_names, None, None, None, None


        token_pos_to_score_pos = {}

        for i, token_pos in enumerate(replace_token_positions):
            token_pos_to_score_pos[token_pos] = i
        # 重新计算Importance score，将所有出现的位置加起来（而不是取平均）.
        names_to_importance_score = {}

        for name in names_positions_dict.keys():
            total_score = 0.0
            positions = names_positions_dict[name]
            for token_pos in positions:
                # 这个token在code中对应的位置
                # importance_score中的位置：token_pos_to_score_pos[token_pos]
                total_score += importance_score[token_pos_to_score_pos[token_pos]]
            
            names_to_importance_score[name] = total_score

        sorted_list_of_names = sorted(names_to_importance_score.items(), key=lambda x: x[1], reverse=True)
        # 根据importance_score进行排序

        nb_changed_var = 0 # 表示被修改的variable数量
        nb_changed_pos = 0
        is_success = -1

        used_substitutes = []
        for name_and_score in sorted_list_of_names:
            tgt_word = name_and_score[0]

            all_substitutes = subs[tgt_word]
            for item in used_substitutes:
                if item in all_substitutes:
                    all_substitutes.remove(item)

            best_loss = math.inf if self.targeted else 0.0
            candidate = None
            replace_examples = []

            substitute_list = []
            for substitute in all_substitutes:
                
                substitute_list.append(substitute)
                # 记录了替换的顺序

                # 需要将几个位置都替换成sustitue_
                temp_code = get_example(adv_code, tgt_word, substitute, "c")               
                new_feature = self.convert_code_to_features(temp_code, self.tokenizer, true_label, self.args)
                replace_examples.append(new_feature)
            if len(replace_examples) == 0:
                # 并没有生成新的mutants，直接跳去下一个token
                continue

            replace_embeddings_list = []
            for feature in replace_examples:
                input_ids, attn_mask, position_idx = self.features_to_model_sub(feature, self.args)
                replace_embeddings_list.append(self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu())
                # 3. 将他们转化成features
            replace_embeddings = torch.stack(replace_embeddings_list)


            if self.targeted:
                for index, embed in enumerate(replace_embeddings):
                    loss = self.loss(embed, target_embeddings)
                    if loss < best_loss:
                        best_loss = loss
                        candidate = substitute_list[index]
                if best_loss < current_loss:
                    print("%s ACC! %s => %s (%.5f => %.5f)" % \
                        ('>>', tgt_word, candidate,
                        current_loss,
                        best_loss), flush=True)
                    nb_changed_var += 1
                    nb_changed_pos += len(names_positions_dict[tgt_word])
                    current_loss = best_loss
                    adv_code = get_example(adv_code, tgt_word, candidate, "c")
                    replaced_words[tgt_word] = candidate
                else:
                    replaced_words[tgt_word] = tgt_word
            else:
                for index, embed in enumerate(replace_embeddings):
                    loss = self.loss(embed, orig_embeddings)
                    if loss > best_loss:
                        best_loss = loss
                        candidate = substitute_list[index]
                if best_loss > current_loss:
                    print("%s ACC! %s => %s (%.5f => %.5f)" % \
                        ('>>', tgt_word, candidate,
                        current_loss,
                        best_loss), flush=True)
                    nb_changed_var += 1
                    nb_changed_pos += len(names_positions_dict[tgt_word])
                    current_loss = best_loss
                    adv_code = get_example(adv_code, tgt_word, candidate, "c")
                    replaced_words[tgt_word] = candidate
                    used_substitutes.append(candidate)
                    # print('word [{}] is removed from the all_substitutes list'.format(candidate))
                else:
                    replaced_words[tgt_word] = tgt_word
            
            if nb_changed_var >= self.args.num_of_changes:
                break
            
            adv_code = adv_code

        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = GraphCodeDataset([adv_feature], self.args)
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('Greedy Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('Greedy Attack Success!!!')
            else:
                is_success = -1


        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



    # def greedy_attack_baseline(self, example, code, subs, target_example=None):
    #     '''
    #     return
    #         original program: code
    #         program length: prog_length
    #         adversar program: adv_program
    #         true label: true_label
    #         original prediction: orig_label
    #         adversarial prediction: temp_label
    #         is_attack_success: is_success
    #         extracted variables: variable_names
    #         importance score of variables: names_to_importance_score
    #         number of changed variables: nb_changed_var
    #         number of changed positions: nb_changed_pos
    #         substitutes for variables: replaced_words
    #     '''
    #         # 先得到tgt_model针对原始Example的预测信息.

    #     # for k, _ in subs.items():
    #     #     subs[k].remove('flat')
    #     # print('removed flat from subs!')

    #     logits, preds = self.model_tgt.get_results([example], 1)
    #     orig_prob = logits[0]
    #     orig_label = preds[0]
    #     true_label = example[1].item()


    #     orig_example = example
    #     orig_code = code
    #     adv_example = example
    #     adv_code = code
    #     orig_embeddings = self.model_sub(orig_example[0].unsqueeze(0).to(self.args.device))[0]


    #     # identifier: the variable names that can be modified
    #     # code_tokens: tokenized code
    #     orig_identifiers, orig_code_tokens = get_identifiers(orig_code, 'c') 
    #     orig_processed_code = " ".join(orig_code_tokens)
    #     # words: tokenized word from the code
    #     # sub_words: fine-grained words
    #     orig_words, orig_sub_words, orig_keys = _tokenize(orig_processed_code, self.tokenizer_mlm)
    #     # 这里经过了小写处理..

    #     adv_embeddings = self.model_sub(adv_example[0].unsqueeze(0).to(self.args.device))[0]

    #     if target_example is not None:
    #         target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
    #         assert orig_embeddings.shape == target_embeddings.shape
        
    #     if self.targeted:
    #         current_loss = self.loss(orig_embeddings, target_embeddings)
    #     else:
    #         current_loss = self.loss(orig_embeddings, adv_embeddings)
        
    #     # identifier: the variable names that can be modified
    #     # code_tokens: tokenized code
    #     identifiers, code_tokens = get_identifiers(adv_code, 'c') 
    #     prog_length = len(code_tokens)

    #     processed_code = " ".join(code_tokens)
    #     adv_words, adv_sub_words, adv_keys = _tokenize(processed_code, self.tokenizer_mlm)
        
    #     # words: tokenized word from the code
    #     # sub_words: fine-grained words
    #     words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
    #     # 这里经过了小写处理..


    #     variable_names = list(subs.keys())  # a list of all variables, including un-identifiers and identifiers
        
    #     if not orig_label == true_label:
    #         # 说明原来就是错的
    #         is_success = -4
    #         temp_label = orig_label
    #         return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None
            
    #     if len(variable_names) == 0:
    #         # 没有提取到identifier，直接退出
    #         is_success = -3
    #         temp_label = orig_label
    #         print('Error! No variable_names extracted!')
    #         return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

    #     sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]

    #     # 计算importance_score.

    #     # name_positions_dict: {key: identifier, value: a list records all the positions that the identifier occurs}
    #     importance_score, replace_token_positions, names_positions_dict = self.get_importance_score( 
    #                                             processed_code,
    #                                             adv_words,
    #                                             adv_sub_words,
    #                                             variable_names,
    #                                             target_example=target_example,)

    #     if importance_score is None:
    #         print('Error! Importance_score is None!')
    #         temp_label = true_label
    #         return code, prog_length, adv_code, true_label, orig_label, temp_label, -3, variable_names, None, None, None, None


    #     token_pos_to_score_pos = {}

    #     for i, token_pos in enumerate(replace_token_positions):
    #         token_pos_to_score_pos[token_pos] = i
    #     # 重新计算Importance score，将所有出现的位置加起来（而不是取平均）.
    #     names_to_importance_score = {}

    #     for name in names_positions_dict.keys():
    #         total_score = 0.0
    #         positions = names_positions_dict[name]
    #         for token_pos in positions:
    #             # 这个token在code中对应的位置
    #             # importance_score中的位置：token_pos_to_score_pos[token_pos]
    #             total_score += importance_score[token_pos_to_score_pos[token_pos]]
            
    #         names_to_importance_score[name] = total_score

    #     sorted_list_of_names = sorted(names_to_importance_score.items(), key=lambda x: x[1], reverse=True)
    #     # 根据importance_score进行排序

    #     nb_changed_var = 0 # 表示被修改的variable数量
    #     nb_changed_pos = 0
    #     is_success = -1
    #     replaced_words = {}

    #     used_substitutes = []
    #     for name_and_score in sorted_list_of_names:
    #         tgt_word = name_and_score[0]

    #         all_substitutes = subs[tgt_word]
    #         for item in used_substitutes:
    #             if item in all_substitutes:
    #                 all_substitutes.remove(item)

    #         best_loss = math.inf if self.targeted else 0.0
    #         candidate = None
    #         replace_examples = []

    #         substitute_list = []
    #         for substitute in all_substitutes:
                
    #             substitute_list.append(substitute)
    #             # 记录了替换的顺序

    #             # 需要将几个位置都替换成sustitue_
    #             temp_code = get_example(adv_code, tgt_word, substitute, "c")
                                                
    #             new_feature = self.convert_code_to_features(temp_code)
    #             replace_examples.append(new_feature.input_ids)
    #         if len(replace_examples) == 0:
    #             # 并没有生成新的mutants，直接跳去下一个token
    #             continue

    #         replace_embeddings_list = []
    #         for example in replace_examples:
    #             replace_embeddings_list.append(self.model_sub(torch.tensor(example).unsqueeze(0).to(self.args.device))[0].detach().cpu())
    #             # 3. 将他们转化成features
    #         replace_embeddings = torch.stack(replace_embeddings_list)


    #         if self.targeted:
    #             for index, embed in enumerate(replace_embeddings):
    #                 loss = self.loss(embed, target_embeddings)
    #                 if loss < best_loss:
    #                     best_loss = loss
    #                     candidate = substitute_list[index]
    #             if best_loss < current_loss:
    #                 print("%s ACC! %s => %s (%.5f => %.5f)" % \
    #                     ('>>', tgt_word, candidate,
    #                     current_loss,
    #                     best_loss), flush=True)
    #                 nb_changed_var += 1
    #                 nb_changed_pos += len(names_positions_dict[tgt_word])
    #                 current_loss = best_loss
    #                 adv_code = get_example(adv_code, tgt_word, candidate, "c")
    #                 replaced_words[tgt_word] = candidate
    #             else:
    #                 replaced_words[tgt_word] = tgt_word
    #         else:
    #             for index, embed in enumerate(replace_embeddings):
    #                 loss = self.loss(embed, orig_embeddings)
    #                 if loss > best_loss:
    #                     best_loss = loss
    #                     candidate = substitute_list[index]
    #             if best_loss > current_loss:
    #                 print("%s ACC! %s => %s (%.5f => %.5f)" % \
    #                     ('>>', tgt_word, candidate,
    #                     current_loss,
    #                     best_loss), flush=True)
    #                 nb_changed_var += 1
    #                 nb_changed_pos += len(names_positions_dict[tgt_word])
    #                 current_loss = best_loss
    #                 adv_code = get_example(adv_code, tgt_word, candidate, "c")
    #                 replaced_words[tgt_word] = candidate
    #                 used_substitutes.append(candidate)
    #                 # print('word [{}] is removed from the all_substitutes list'.format(candidate))
    #             else:
    #                 replaced_words[tgt_word] = tgt_word
            
    #         adv_code = adv_code

    #     #  query the model_tgt to see whether the attack is success
    #     adv_feature = self.convert_code_to_features(adv_code)
    #     adv_feature.label = 0    # set a pseduo label
    #     adv_dataset = CodeDataset([adv_feature])
    #     logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
    #     logit, temp_label = logits[0], preds[0]
    #     if self.targeted:
    #         target_label = target_example[1]
    #         if temp_label == target_label:
    #             is_success = 1
    #             print('Greedy Attack Success!!!')
    #         else:
    #             is_success = -1
    #     else:
    #         if temp_label != true_label:
    #             is_success = 1
    #             print('Greedy Attack Success!!!')
    #         else:
    #             is_success = -1

    #     adv_example = (torch.tensor(adv_feature.input_ids), true_label)

    #     return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words




    # def ga_attack(self, example, code, subs, initial_replace=None, target_example=None):
    #     '''
    #     return
    #         original program: code
    #         program length: prog_length
    #         adversar program: adv_program
    #         true label: true_label
    #         original prediction: orig_label
    #         adversarial prediction: temp_label
    #         is_attack_success: is_success
    #         extracted variables: variable_names
    #         importance score of variables: names_to_importance_score
    #         number of changed variables: nb_changed_var
    #         number of changed positions: nb_changed_pos
    #         substitutes for variables: replaced_words
    #     '''
    #         # 先得到tgt_model针对原始Example的预测信息.


    #     logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
    #     orig_prob = logits[0]
    #     orig_label = preds[0]
    #     true_label = example[1]

    #     orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
    #     # logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
    #     if target_example is not None:
    #         target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
    #         print('orig_embeddings.shape: {}, target_embeddings.shape: {}'.format(orig_embeddings.shape, target_embeddings.shape))
    #         assert orig_embeddings.shape == target_embeddings.shape
        
    #     if self.targeted:
    #         current_loss = self.loss(orig_embeddings, target_embeddings)
    #     else:
    #         current_loss = 0.0

    #     adv_code = code

    #     temp_label = None

    #     identifiers, code_tokens = get_identifiers(code, 'c')
    #     prog_length = len(code_tokens)


    #     processed_code = " ".join(code_tokens)
        
    #     words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
    #     # 这里经过了小写处理..


    #     variable_names = list(subs.keys())

    #     if not orig_label == true_label:
    #         # 说明原来就是错的
    #         is_success = -4
    #         temp_label = orig_label
    #         return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None
            
    #     if len(variable_names) == 0:
    #         # 没有提取到identifier，直接退出
    #         is_success = -3
    #         return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

    #     names_positions_dict = get_identifier_posistions_from_code(words, variable_names)

    #     nb_changed_var = 0 # 表示被修改的variable数量
    #     nb_changed_pos = 0
    #     is_success = -1

    #     # 我们可以先生成所有的substitutes
    #     variable_substitute_dict = {}

    #     for tgt_word in names_positions_dict.keys():
    #         variable_substitute_dict[tgt_word] = subs[tgt_word]

    #     fitness_values = []
    #     base_chromesome = {word: word for word in variable_substitute_dict.keys()}
    #     population = [base_chromesome]
    #     # 关于chromesome的定义: {tgt_word: candidate, tgt_word_2: candidate_2, ...}
    #     for tgt_word in variable_substitute_dict.keys():
    #         # 这里进行初始化
    #         if initial_replace is None:
    #             # 对于每个variable: 选择"影响最大"的substitutes
    #             replace_examples = []
    #             substitute_list = []
                
    #             best_loss = math.inf if self.targeted else 0.0
    #             initial_candidate = tgt_word
    #             tgt_positions = names_positions_dict[tgt_word]
                
    #             # 原来是随机选择的，现在要找到改变最大的.
    #             for a_substitute in variable_substitute_dict[tgt_word]:
    #                 # a_substitute = a_substitute.strip()
                    
    #                 substitute_list.append(a_substitute)
    #                 # 记录下这次换的是哪个substitute
    #                 temp_code = get_example(code, tgt_word, a_substitute, "c") 
    #                 new_feature = self.convert_code_to_features(temp_code)
    #                 replace_examples.append(new_feature.input_ids)

    #             if len(replace_examples) == 0:
    #                 # 并没有生成新的mutants，直接跳去下一个token
    #                 continue

    #             replace_embeddings_list = []
    #             for example in replace_examples:
    #                 replace_embeddings_list.append(self.model_sub(torch.tensor(example).unsqueeze(0).to(self.args.device))[0].detach().cpu())
    #                 # 3. 将他们转化成features
    #             replace_embeddings = torch.stack(replace_embeddings_list)

    #             _the_best_candidate = -1
    #             if self.targeted:
    #                 for index, embed in enumerate(replace_embeddings):
    #                     loss = self.loss(embed, target_embeddings)
    #                     if loss < best_loss:
    #                         best_loss = loss
    #                         _the_best_candidate = index
    #             else:
    #                 for index, embed in enumerate(replace_embeddings):
    #                     loss = self.loss(embed, orig_embeddings)
    #                     if loss > best_loss:
    #                         best_loss = loss
    #                         _the_best_candidate = index
    #             if _the_best_candidate == -1:
    #                 initial_candidate = tgt_word
    #             else:
    #                 initial_candidate = substitute_list[_the_best_candidate]
    #         else:
    #             initial_candidate = initial_replace[tgt_word]

    #         temp_chromesome = copy.deepcopy(base_chromesome)
    #         temp_chromesome[tgt_word] = initial_candidate
    #         population.append(temp_chromesome)
    #         if target_example is not None:
    #             temp_fitness = self.compute_fitness(temp_chromesome, self.model_tgt, self.tokenizer, max(orig_prob), orig_label, true_label ,code, names_positions_dict, self.args, orig_example=example, target_example=target_example)
    #         else:
    #             temp_fitness = self.compute_fitness(temp_chromesome, self.model_tgt, self.tokenizer, max(orig_prob), orig_label, true_label ,code, names_positions_dict, self.args, orig_example=example, target_example=None)
    #         fitness_values.append(temp_fitness)

    #     cross_probability = 0.7

    #     max_iter = max(5 * len(population), 10)
    #     # 这里的超参数还是得调试一下.

    #     for i in range(max_iter):
    #         _temp_mutants = []
    #         for j in range(self.args.eval_batch_size):
    #             p = random.random()
    #             chromesome_1, index_1, chromesome_2, index_2 = select_parents(population)
    #             if p < cross_probability: # 进行crossover
    #                 if chromesome_1 == chromesome_2:
    #                     child_1 = mutate(chromesome_1, variable_substitute_dict)
    #                     continue
    #                 child_1, child_2 = crossover(chromesome_1, chromesome_2)
    #                 if child_1 == chromesome_1 or child_1 == chromesome_2:
    #                     child_1 = mutate(chromesome_1, variable_substitute_dict)
    #             else: # 进行mutates
    #                 child_1 = mutate(chromesome_1, variable_substitute_dict)
    #             _temp_mutants.append(child_1)
            
    #         # compute fitness in batch
    #         feature_list = []
    #         for mutant in _temp_mutants:
    #             _temp_code = map_chromesome(mutant, code, "c")
    #             _tmp_feature = self.convert_code_to_features(_temp_code)
    #             feature_list.append(_tmp_feature.input_ids)
    #         if len(feature_list) == 0:
    #             continue
    #         # mutate_logits, mutate_preds = self.model_tgt.get_results(new_dataset, self.args.eval_batch_size)
    #         mutate_embeddings_list = []
    #         for feature in feature_list:
    #             mutate_embeddings_list.append(self.model_sub(torch.tensor(feature).unsqueeze(0).to(self.args.device))[0].detach().cpu())
    #         mutate_embeddings = torch.stack(mutate_embeddings_list)
    #         mutate_fitness_values = []
    #         for index, mutate_embed in enumerate(mutate_embeddings):
    #             if self.targeted:
    #                 _tmp_fitness = -self.loss(mutate_embed, target_embeddings)
    #                 mutate_fitness_values.append(_tmp_fitness)
    #             else:
    #                 _tmp_fitness = self.loss(mutate_embed, orig_embeddings)
    #                 mutate_fitness_values.append(_tmp_fitness)
                
    #         # 现在进行替换.
    #         for index, fitness_value in enumerate(mutate_fitness_values):
    #             min_value = min(fitness_values)
    #             if fitness_value > min_value:
    #                 # 替换.
    #                 min_index = fitness_values.index(min_value)
    #                 population[min_index] = _temp_mutants[index]
    #                 fitness_values[min_index] = fitness_value

    #     best_index = 0
    #     best_fitness = 0
    #     for index, fitness_value in enumerate(fitness_values):
    #         if fitness_value > best_fitness:
    #             best_index = index
    #             best_fitness = fitness_value

    #     adv_code = map_chromesome(population[best_index], code, "c")
    #     for old_word in population[best_index].keys():
    #         if old_word == population[index][old_word]:
    #             nb_changed_var += 1
    #             nb_changed_pos += len(names_positions_dict[old_word])

        
    #     #  query the model_tgt to see whether the attack is success
    #     adv_feature = self.convert_code_to_features(adv_code)
    #     adv_feature.label = 0    # set a pseduo label
    #     adv_dataset = CodeDataset([adv_feature])
    #     logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
    #     logit, temp_label = logits[0], preds[0]
    #     if self.targeted:
    #         target_label = target_example[1]
    #         if temp_label == target_label:
    #             is_success = 1
    #             print('GA Attack Success!!!')
    #         else:
    #             is_success = -1
    #     else:
    #         if temp_label != true_label:
    #             is_success = 1
    #             print('GA Attack Success!!!')
    #         else:
    #             is_success = -1

    #     return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, nb_changed_var, nb_changed_pos, None
    


    def insert_attack(self, example, code, subs, target_example=None):
        def get_insert_masked_code(code, pos):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split(';')
            splited_code.insert(pos, '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '; ')
            return inserted_code_str

        def get_inserted_code(code, pos, variable_statement):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split(';')
            splited_code.insert(pos, variable_statement)
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + ';')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[3].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device), example[1].unsqueeze(0).to(self.args.device), example[2].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        
        prog_length = 0

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall(';', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            masked_feature = self.convert_code_to_features(masked_code, self.tokenizer, true_label, self.args)
            input_ids, attn_mask, position_idx = self.features_to_model_sub(masked_feature, self.args)
            masked_embeddings = self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        for k, v in subs.items():
            global subs_for_insert 
            subs_for_insert = v

        subs_for_insert = subs_for_insert[:60]  
        print('length of subs_for_insert: {}'.format(len(subs_for_insert)))

        #剔除原代码中的变量名
        # subs_var = subs_for_insert
        # for used_var in identifiers:
        #     used_var = used_var[0]
        #     if used_var in subs_var:
        #         subs_var.remove(used_var)

        print('Insertable num: ', len(sorted_id))
        inserted_num = 0
        for i, insert_idx in enumerate(sorted_id):
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, insert_idx, 'char temp_variable[100] = ' + '"' + str(sub) + '"')
                adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
                input_ids, attn_mask, position_idx = self.features_to_model_sub(adv_feature, self.args)
                adv_embeddings = self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu()
                loss_value = self.loss(orig_embeddings, adv_embeddings)
                if loss_value > temp_best_loss:
                    temp_best_loss = loss_value
                    temp_best_code = adv_code
                    update_flag = True

            final_code = temp_best_code
            
            if update_flag:
                for idx in range(len(sorted_id)):
                    if sorted_id[idx] >= insert_idx:
                        sorted_id[idx] += 1
                inserted_num += 1
                #控制插入数量
            if inserted_num >= self.args.num_of_changes:
                break

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = GraphCodeDataset([adv_feature], self.args)
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('Insert Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('Insert Attack Success!!!')
            else:
                is_success = -1

        print('success: {}, adv_code: {}'.format(is_success, final_code))

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = [], None, None, None

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words


    def empty_print_attack(self, example, code, subs, target_example=None):
        def get_insert_masked_code(code, pos):

            splited_code = code.split(';')
            splited_code.insert(pos, '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '; ')
            return inserted_code_str


        def get_inserted_code(code, pos, variable_statement='printf("")'):

            splited_code = code.split(';')
            splited_code.insert(pos, variable_statement)
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '; ')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[3].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device), example[1].unsqueeze(0).to(self.args.device), example[2].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        prog_length = 0

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        insert_pos_nums = len(re.findall(';', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            masked_feature = self.convert_code_to_features(masked_code, self.tokenizer, true_label, self.args)
            input_ids, attn_mask, position_idx = self.features_to_model_sub(masked_feature, self.args)
            masked_embeddings = self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        inserted_num = 0
        for i, inserted_id in enumerate(sorted_id):
            update_flag = False
            adv_code = get_inserted_code(final_code, inserted_id)
            adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
            input_ids, attn_mask, position_idx = self.features_to_model_sub(adv_feature, self.args)
            adv_embeddings = self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            loss_value = self.loss(orig_embeddings, adv_embeddings)

            if loss_value > temp_best_loss:
                temp_best_loss = loss_value
                temp_best_code = adv_code
                update_flag = True

            final_code = temp_best_code
            if update_flag:
                for idx in range(len(sorted_id)):
                    if sorted_id[idx] >= inserted_id:
                        sorted_id[idx] += 1
                inserted_num += 1
            if inserted_num >= self.args.num_of_changes:
                break

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = GraphCodeDataset([adv_feature], self.args)
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('Insert Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('Insert Attack Success!!!')
            else:
                is_success = -1

        print('success: {}, adv_code: {}'.format(is_success, final_code))

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = None, None, None, None

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words




    def nonreachable_if_attack(self, example, code, subs, target_example=None):
        def get_insert_masked_code(code, pos):
            splited_code = code.split('\n')
            splited_code.insert(pos, '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '; ')
            return inserted_code_str


        def get_inserted_code(code, pos, print_statement):
            splited_code = code.split(';')
            splited_code.insert(pos, 'if (0): {{ printf("{}") }}'.format(print_statement))
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + ';')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[3].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device), example[1].unsqueeze(0).to(self.args.device), example[2].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        prog_length = 0

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        insert_pos_nums = len(re.findall(';', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            masked_feature = self.convert_code_to_features(masked_code, self.tokenizer, true_label, self.args)
            input_ids, attn_mask, position_idx = self.features_to_model_sub(masked_feature, self.args)
            masked_embeddings = self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        for k, v in subs.items():
            global subs_for_insert 
            subs_for_insert = v

        subs_for_insert = subs_for_insert[:60]  
        print('length of subs_for_insert: {}'.format(len(subs_for_insert)))

        inserted_num = 0
        for i, inserted_id in enumerate(sorted_id):
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, inserted_id, str(sub))
                adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
                input_ids, attn_mask, position_idx = self.features_to_model_sub(adv_feature, self.args)
                adv_embeddings = self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu()
                loss_value = self.loss(orig_embeddings, adv_embeddings)
                if loss_value > temp_best_loss:
                    temp_best_loss = loss_value
                    temp_best_code = adv_code
                    update_flag = True

            final_code = temp_best_code

            if update_flag:
                for idx in range(len(sorted_id)):
                    if sorted_id[idx] >= inserted_id:
                        sorted_id[idx] += 1
                inserted_num += 1
            # print('inserted_num: {}, self.args.num_of_changes: {}'.format(inserted_num, self.args.num_of_changes))
            if inserted_num >= self.args.num_of_changes:
                break

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = GraphCodeDataset([adv_feature], self.args)
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('Insert Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('Insert Attack Success!!!')
            else:
                is_success = -1

        print('success: {}, adv_code: {}'.format(is_success, final_code))

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = None, None, None, None

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



    def nonreachable_while_attack(self, example, code, subs, target_example=None):
        def get_insert_masked_code(code, pos):

            splited_code = code.split(';')
            splited_code.insert(pos, '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + ';')
            return inserted_code_str


        def get_inserted_code(code, pos, print_statement):

            splited_code = code.split(';')
            splited_code.insert(pos, 'while (0): {{ print("{}"); }}'.format(print_statement))
            inserted_code_str = ''
            for index, line in enumerate(splited_code):
                if index != pos:
                    inserted_code_str += (line) + ';'
                else:
                    inserted_code_str += (line)
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[3].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device), example[1].unsqueeze(0).to(self.args.device), example[2].unsqueeze(0).to(self.args.device))[0]
        
        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        
        prog_length = 0

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        for k, v in subs.items():
            global subs_for_insert 
            subs_for_insert = v

        subs_for_insert = subs_for_insert[:60]  
        print('length of subs_for_insert: {}'.format(len(subs_for_insert)))


        insert_pos_nums = len(re.findall(';', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            masked_feature = self.convert_code_to_features(masked_code, self.tokenizer, true_label, self.args)
            input_ids, attn_mask, position_idx = self.features_to_model_sub(masked_feature, self.args)
            masked_embeddings = self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        inserted_num = 0
        for i, inserted_id in enumerate(sorted_id):
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, inserted_id, str(sub))
                adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
                input_ids, attn_mask, position_idx = self.features_to_model_sub(adv_feature, self.args)
                adv_embeddings = self.model_sub(torch.tensor(input_ids).unsqueeze(0).to(self.args.device), torch.tensor(attn_mask).unsqueeze(0).to(self.args.device), torch.tensor(position_idx).unsqueeze(0).to(self.args.device))[0].detach().cpu()
                loss_value = self.loss(orig_embeddings, adv_embeddings)
                if loss_value > temp_best_loss:
                    temp_best_loss = loss_value
                    temp_best_code = adv_code
                    update_flag = True
            final_code = temp_best_code
            if update_flag:
                for idx in range(len(sorted_id)):
                    if sorted_id[idx] >= inserted_id:
                        sorted_id[idx] += 1
                inserted_num += 1
            # print('inserted_num: {}, self.args.num_of_changes: {}'.format(inserted_num, self.args.num_of_changes))
            if inserted_num >= self.args.num_of_changes:
                break

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code, self.tokenizer, true_label, self.args)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = GraphCodeDataset([adv_feature], self.args)
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('Insert Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('Insert Attack Success!!!')
            else:
                is_success = -1

        print('success: {}, adv_code: {}'.format(is_success, final_code))

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = None, None, None, None

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



# class MHM_Attacker():
#     def __init__(self, args, model_sub, model_tgt, model_mlm, tokenizer_mlm) -> None:
#         self.model_sub = model_sub
#         self.classifier = model_tgt
#         self.tokenizer = tokenizer_mlm
#         self.model_mlm = model_mlm
#         # self.token2idx = _token2idx
#         # self.idx2token = _idx2token
#         self.args = args
#         self.tokenizer_mlm = tokenizer_mlm

#     def convert_code_to_features(self, code):
#         code=' '.join(code.split())
#         code_tokens=self.tokenizer.tokenize(code)[:self.args.block_size-2]
#         source_tokens =[self.tokenizer.cls_token]+code_tokens+[self.tokenizer.sep_token]
#         source_ids =  self.tokenizer.convert_tokens_to_ids(source_tokens)
#         padding_length = self.args.block_size - len(source_ids)
#         source_ids+=[self.tokenizer.pad_token_id]*padding_length
#         return InputFeatures(source_tokens,source_ids, 0, 0)


#     def get_feature_distance(self, orig_embeddings, adv_code):
#         adv_code = ' ' + adv_code
#         adv_feature = self.convert_code_to_features(adv_code).input_ids
#         adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0]
#         return nn.MSELoss()(orig_embeddings.to(self.args.device), adv_embeddings.to(self.args.device)).item()

    
#     def mcmc(self, example, tokenizer, substituions, code=None, _label=None, _n_candi=30,
#              _max_iter=100, _prob_threshold=0.95):

#         self.orig_embeddings = self.model_sub(example[0].view(-1,self.args.block_size).to(self.args.device))[0]

#         logits, preds = self.classifier.get_results([example], self.args.eval_batch_size)
#         orig_prob = logits[0]
#         orig_label = preds[0]
#         true_label = example[1].item()
#         adv_code = copy.deepcopy(code)


#         identifiers, code_tokens = get_identifiers(code, 'c')
#         prog_length = len(code_tokens)
#         processed_code = " ".join(code_tokens)

#         words, sub_words, keys = _tokenize(processed_code, tokenizer)
#         raw_tokens = copy.deepcopy(words)
#         variable_names = list(substituions.keys())
        
#         if not orig_label == true_label:
#             # 说明原来就是错的
#             is_success = -4
#             return {'succ': is_success, 'adv_code': adv_code, 'tokens': None, 'raw_tokens': None}

#         uid = get_identifier_posistions_from_code(words, variable_names)

#         if len(uid) <= 0: # 是有可能存在找不到变量名的情况的.
#             is_success = -3
#             return {'succ': is_success, 'adv_code': adv_code, 'tokens': None, 'raw_tokens': None}


#         variable_substitue_dict = {}

#         for tgt_word in uid.keys():
#             variable_substitue_dict[tgt_word] = substituions[tgt_word]

#         if len(variable_substitue_dict) <= 0: # 是有可能存在找不到变量名的情况的.
#             is_success = -3
#             return {'succ': is_success, 'adv_code': adv_code, 'tokens': None, 'raw_tokens': None}

#         old_uids = {}
#         old_uid = ""
#         for iteration in range(1, 1+_max_iter):
#             # 这个函数需要tokens
#             res = self.__replaceUID(_tokens=code, _label=_label, _uid=uid,
#                                     substitute_dict=variable_substitue_dict,
#                                     _n_candi=_n_candi,
#                                     _prob_threshold=_prob_threshold)
#             self.__printRes(_iter=iteration, _res=res, _prefix="  >> ")

#             if res['status'].lower() in ['s', 'a']:
#                 if iteration == 1:
#                     old_uids[res["old_uid"]] = []
#                     old_uids[res["old_uid"]].append(res["new_uid"])
#                     old_uid = res["old_uid"]
                    
#                 flag = 0
#                 for k in old_uids.keys():
#                     if res["old_uid"] == old_uids[k][-1]:
#                         flag = 1
#                         old_uids[k].append(res["new_uid"])
#                         old_uid = k
#                         break
#                 if flag == 0:
#                     old_uids[res["old_uid"]] = []
#                     old_uids[res["old_uid"]].append(res["new_uid"])
#                     old_uid = res["old_uid"]

#                 code = res['tokens']
#                 uid[res['new_uid']] = uid.pop(res['old_uid']) # 替换key，但保留value.
#                 variable_substitue_dict[res['new_uid']] = variable_substitue_dict.pop(res['old_uid'])
#                 for i in range(len(raw_tokens)):
#                     if raw_tokens[i] == res['old_uid']:
#                         raw_tokens[i] = res['new_uid']
#                 # if res['status'].lower() == 's':
#                 #     replace_info = {}
#                 #     nb_changed_pos = 0
#                 #     for uid_ in old_uids.keys():
#                 #         replace_info[uid_] = old_uids[uid_][-1]
#                 #         nb_changed_pos += len(uid[old_uids[uid_][-1]])
#                 #     return {'succ': True, 'tokens': code,
#                 #             'raw_tokens': raw_tokens, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": 1, "old_uid": old_uid, "score_info": res["old_prob"][0]-res["new_prob"][0], "nb_changed_var": len(old_uids), "nb_changed_pos": nb_changed_pos, "replace_info": replace_info, "attack_type": "MHM"}
#         replace_info = {}
#         nb_changed_pos = 0
#         for uid_ in old_uids.keys():
#             replace_info[uid_] = old_uids[uid_][-1]
#             nb_changed_pos += len(uid[old_uids[uid_][-1]])

#         adv_code = code
#         #  query the model_tgt to see whether the attack is success
#         adv_feature = self.convert_code_to_features(adv_code)
#         adv_feature.label = 0    # set a pseduo label
#         adv_dataset = CodeDataset([adv_feature])
#         logits, preds = self.classifier.get_results(adv_dataset, self.args.eval_batch_size)
#         logit, temp_label = logits[0], preds[0]
#         if temp_label != _label:
#             is_success = 1
#             print('MHM Attack Success!!!')
#         else:
#             is_success = -1

#         return {'succ': is_success, 'adv_code': adv_code, 'tokens': res['tokens'], 'raw_tokens': None, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": -1, "old_uid": old_uid, "score_info": res["old_prob"]-res["new_prob"], "nb_changed_var": len(old_uids), "nb_changed_pos": nb_changed_pos, "replace_info": replace_info, "attack_type": "MHM"}


    # def mcmc_random(self, tokenizer, substituions, code=None, _label=None, _n_candi=30,
    #          _max_iter=100, _prob_threshold=0.95):
    #     identifiers, code_tokens = get_identifiers(code, 'c')
    #     processed_code = " ".join(code_tokens)
    #     prog_length = len(code_tokens)
    #     words, sub_words, keys = _tokenize(processed_code, tokenizer)
    #     raw_tokens = copy.deepcopy(words)
    #     variable_names = list(substituions.keys())

    #     uid = get_identifier_posistions_from_code(words, variable_names)

    #     if len(uid) <= 0: # 是有可能存在找不到变量名的情况的.
    #         return {'succ': None, 'tokens': None, 'raw_tokens': None}

    #     variable_substitue_dict = {}
    #     for tgt_word in uid.keys():
    #         variable_substitue_dict[tgt_word] = substituions[tgt_word]

    #     old_uids = {}
    #     old_uid = ""
    #     for iteration in range(1, 1+_max_iter):
    #         # 这个函数需要tokens
    #         res = self.__replaceUID_random(_tokens=code, _label=_label, _uid=uid,
    #                                 substitute_dict=variable_substitue_dict,
    #                                 _n_candi=_n_candi,
    #                                 _prob_threshold=_prob_threshold)
    #         self.__printRes(_iter=iteration, _res=res, _prefix="  >> ")

    #         if res['status'].lower() in ['s', 'a']:
    #             if iteration == 1:
    #                 old_uids[res["old_uid"]] = []
    #                 old_uids[res["old_uid"]].append(res["new_uid"])
    #                 old_uid = res["old_uid"]

    #             flag = 0
    #             for k in old_uids.keys():
    #                 if res["old_uid"] == old_uids[k][-1]:
    #                     flag = 1
    #                     old_uids[k].append(res["new_uid"])
    #                     old_uid = k
    #                     break
    #             if flag == 0:
    #                 old_uids[res["old_uid"]] = []
    #                 old_uids[res["old_uid"]].append(res["new_uid"])
    #                 old_uid = res["old_uid"]
                
                    
    #             code = res['tokens']
    #             uid[res['new_uid']] = uid.pop(res['old_uid']) # 替换key，但保留value.
    #             variable_substitue_dict[res['new_uid']] = variable_substitue_dict.pop(res['old_uid'])
                
    #             for i in range(len(raw_tokens)):
    #                 if raw_tokens[i] == res['old_uid']:
    #                     raw_tokens[i] = res['new_uid']
    #             if res['status'].lower() == 's':
    #                 replace_info = {}
    #                 nb_changed_pos = 0
    #                 for uid_ in old_uids.keys():
    #                     replace_info[uid_] = old_uids[uid_][-1]
    #                     nb_changed_pos += len(uid[old_uids[uid_][-1]])
    #                 return {'succ': True, 'tokens': code,
    #                         'raw_tokens': raw_tokens, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": 1, "old_uid": old_uid, "score_info": res["old_prob"][0]-res["new_prob"][0], "nb_changed_var": len(old_uids), "nb_changed_pos": nb_changed_pos, "replace_info": replace_info, "attack_type": "MHM-Origin"}
    #     replace_info = {}
    #     nb_changed_pos = 0

    #     for uid_ in old_uids.keys():
    #         replace_info[uid_] = old_uids[uid_][-1]
    #         nb_changed_pos += len(uid[old_uids[uid_][-1]])
        
    #     return {'succ': False, 'tokens': res['tokens'], 'raw_tokens': None, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": -1, "old_uid": old_uid, "score_info": res["old_prob"][0]-res["new_prob"][0], "nb_changed_var": len(old_uids), "nb_changed_pos": nb_changed_pos, "replace_info": replace_info, "attack_type": "MHM-Origin"}
    
    def __replaceUID(self, _tokens, _label=None, _uid={}, substitute_dict={},
                     _n_candi=30, _prob_threshold=0.95, _candi_mode="random"):
        
        assert _candi_mode.lower() in ["random", "nearby"]
        
        selected_uid = random.sample(substitute_dict.keys(), 1)[0] # 选择需要被替换的变量名
        if _candi_mode == "random":
            # First, generate candidate set.
            # The transition probabilities of all candidate are the same.
            candi_token = [selected_uid]
            candi_tokens = [copy.deepcopy(_tokens)]
            candi_labels = [_label]
            for c in random.sample(substitute_dict[selected_uid], min(_n_candi, len(substitute_dict[selected_uid]))): # 选出_n_candi数量的候选.
                if c in _uid.keys():
                    continue
                if isUID(c): # 判断是否是变量名.
                    candi_token.append(c)
                    candi_tokens.append(copy.deepcopy(_tokens))
                    candi_labels.append(_label)
                    candi_tokens[-1] = get_example(candi_tokens[-1], selected_uid, c, "c")
                    # for i in _uid[selected_uid]: # 依次进行替换.
                    #     if i >= len(candi_tokens[-1]):
                    #         break
                    #     candi_tokens[-1][i] = c # 替换为新的candidate.

            feature_distances = []
            for tmp_tokens in candi_tokens:
                tmp_tokens = "".join(tmp_tokens.split())
                feature_distances.append(self.get_feature_distance(self.orig_embeddings, tmp_tokens))

            best_dist = feature_distances[0]
            best_code = candi_tokens[0]
            best_token = candi_token[0]
            for i in range(len(candi_token)):   # Find a valid example
                if feature_distances[i] > best_dist:
                    # print('feature_distances[{}] = {}'.format(i, feature_distances[i]))
                    best_dist = feature_distances[i]
                    best_code = candi_tokens[i]
                    best_token = candi_token[i]
            return {"status": "a", "alpha": 1, "tokens": best_code,
                    "old_uid": selected_uid, "new_uid": best_token,
                    "old_prob": feature_distances[0], "new_prob": best_dist,
                    "old_pred": feature_distances[0], "new_pred": best_dist, "nb_changed_pos": _tokens.count(selected_uid)}


        #     new_example = []
        #     for tmp_tokens in candi_tokens:
        #         tmp_code = tmp_tokens
        #         new_feature = convert_code_to_features(tmp_code, self.tokenizer_mlm, _label, self.args)
        #         new_example.append(new_feature)
        #     new_dataset = CodeDataset(new_example)
        #     prob, pred = self.classifier.get_results(new_dataset, self.args.eval_batch_size)

        #     for i in range(len(candi_token)):   # Find a valid example
        #         if pred[i] != _label: # 如果有样本攻击成功
        #             return {"status": "s", "alpha": 1, "tokens": candi_tokens[i],
        #                     "old_uid": selected_uid, "new_uid": candi_token[i],
        #                     "old_prob": prob[0], "new_prob": prob[i],
        #                     "old_pred": pred[0], "new_pred": pred[i], "nb_changed_pos": _tokens.count(selected_uid)}

        #     candi_idx = 0
        #     min_prob = 1.0

        #     for idx, a_prob in enumerate(prob[1:]):
        #         if a_prob[_label] < min_prob:
        #             candi_idx = idx + 1
        #             min_prob = a_prob[_label]

        #     # 找到Ground_truth对应的probability最小的那个mutant
        #     # At last, compute acceptance rate.
        #     alpha = (1-prob[candi_idx][_label]+1e-10) / (1-prob[0][_label]+1e-10)
        #     # 计算这个id对应的alpha值.
        #     if random.uniform(0, 1) > alpha or alpha < _prob_threshold:
        #         return {"status": "r", "alpha": alpha, "tokens": candi_tokens[i],
        #                 "old_uid": selected_uid, "new_uid": candi_token[i],
        #                 "old_prob": prob[0], "new_prob": prob[i],
        #                 "old_pred": pred[0], "new_pred": pred[i], "nb_changed_pos": _tokens.count(selected_uid)}
        #     else:
        #         return {"status": "a", "alpha": alpha, "tokens": candi_tokens[i],
        #                 "old_uid": selected_uid, "new_uid": candi_token[i],
        #                 "old_prob": prob[0], "new_prob": prob[i],
        #                 "old_pred": pred[0], "new_pred": pred[i], "nb_changed_pos": _tokens.count(selected_uid)}
        # else:
        #     pass


    # def __replaceUID_random(self, _tokens, _label=None, _uid={}, substitute_dict={},
    #                  _n_candi=30, _prob_threshold=0.95, _candi_mode="random"):
        
    #     assert _candi_mode.lower() in ["random", "nearby"]
        
    #     selected_uid = random.sample(substitute_dict.keys(), 1)[0] # 选择需要被替换的变量名
    #     if _candi_mode == "random":
    #         # First, generate candidate set.
    #         # The transition probabilities of all candidate are the same.
    #         candi_token = [selected_uid]
    #         candi_tokens = [copy.deepcopy(_tokens)]
    #         candi_labels = [_label]
    #         for c in random.sample(self.idx2token, _n_candi): # 选出_n_candi数量的候选.
    #             if c in _uid.keys():
    #                 continue
    #             if isUID(c): # 判断是否是变量名.
    #                 candi_token.append(c)
    #                 candi_tokens.append(copy.deepcopy(_tokens))
    #                 candi_labels.append(_label)
    #                 candi_tokens[-1] = get_example(candi_tokens[-1], selected_uid, c, "c")
    #                 # for i in _uid[selected_uid]: # 依次进行替换.
    #                 #     if i >= len(candi_tokens[-1]):
    #                 #         break
    #                 #     candi_tokens[-1][i] = c # 替换为新的candidate.
            
    #         new_example = []
    #         for tmp_tokens in candi_tokens:
    #             tmp_code = tmp_tokens
    #             new_feature = self.convert_code_to_features(tmp_code, self.tokenizer_mlm, _label, self.args)
    #             new_example.append(new_feature)
    #         new_dataset = CodeDataset(new_example)
    #         prob, pred = self.classifier.get_results(new_dataset, self.args.eval_batch_size)

    #         for i in range(len(candi_token)):   # Find a valid example
    #             if pred[i] != _label: # 如果有样本攻击成功
    #                 return {"status": "s", "alpha": 1, "tokens": candi_tokens[i],
    #                         "old_uid": selected_uid, "new_uid": candi_token[i],
    #                         "old_prob": prob[0], "new_prob": prob[i],
    #                         "old_pred": pred[0], "new_pred": pred[i], "nb_changed_pos": _tokens.count(selected_uid)}

    #         candi_idx = 0
    #         min_prob = 1.0

    #         for idx, a_prob in enumerate(prob[1:]):
    #             if a_prob[_label] < min_prob:
    #                 candi_idx = idx + 1
    #                 min_prob = a_prob[_label]

    #         # 找到Ground_truth对应的probability最小的那个mutant
    #         # At last, compute acceptance rate.
    #         alpha = (1-prob[candi_idx][_label]+1e-10) / (1-prob[0][_label]+1e-10)
    #         # 计算这个id对应的alpha值.
    #         if random.uniform(0, 1) > alpha or alpha < _prob_threshold:
    #             return {"status": "r", "alpha": alpha, "tokens": candi_tokens[i],
    #                     "old_uid": selected_uid, "new_uid": candi_token[i],
    #                     "old_prob": prob[0], "new_prob": prob[i],
    #                     "old_pred": pred[0], "new_pred": pred[i], "nb_changed_pos": _tokens.count(selected_uid)}
    #         else:
    #             return {"status": "a", "alpha": alpha, "tokens": candi_tokens[i],
    #                     "old_uid": selected_uid, "new_uid": candi_token[i],
    #                     "old_prob": prob[0], "new_prob": prob[i],
    #                     "old_pred": pred[0], "new_pred": pred[i], "nb_changed_pos": _tokens.count(selected_uid)}
    #     else:
    #         pass

    def __printRes(self, _iter=None, _res=None, _prefix="  => "):
        if _res['status'].lower() == 's':   # Accepted & successful
            print("%s iter %d, SUCC! %s => %s (%d => %d, %.5f => %.5f) a=%.3f" % \
                  (_prefix, _iter, _res['old_uid'], _res['new_uid'],
                   _res['old_pred'], _res['new_pred'],
                   _res['old_prob'][_res['old_pred']],
                   _res['new_prob'][_res['old_pred']], _res['alpha']), flush=True)
        elif _res['status'].lower() == 'r': # Rejected
            print("%s iter %d, REJ. %s => %s (%d => %d, %.5f => %.5f) a=%.3f" % \
                  (_prefix, _iter, _res['old_uid'], _res['new_uid'],
                   _res['old_pred'], _res['new_pred'],
                   _res['old_prob'][_res['old_pred']],
                   _res['new_prob'][_res['old_pred']], _res['alpha']), flush=True)
        elif _res['status'].lower() == 'a': # Accepted
            print("%s iter %d, ACC! %s => %s (%.5f => %.5f)" % \
                  (_prefix, _iter, _res['old_uid'], _res['new_uid'],
                   _res['old_pred'], _res['new_pred']), flush=True)