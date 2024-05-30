import sys
import os

sys.path.append('../../../')
sys.path.append('../../../python_parser')

import copy
import random
import re
import math
import torch
import torch.nn as nn
import numpy as np
from model import Model
from run import TextDataset, InputFeatures
from utils import select_parents, crossover, map_chromesome, mutate, is_valid_variable_name, _tokenize, get_identifier_posistions_from_code, get_masked_code_by_position, get_substitutes, is_valid_substitute, set_seed

from utils import CodeDataset
from utils import getUID, isUID, getTensor, build_vocab
from run_parser import get_identifiers, get_example
from transformers import (RobertaForMaskedLM, RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer)


class CrossDomainAttacker():
    def __init__(self, args, model_sub, model_tgt, tokenizer, model_mlm, tokenizer_mlm, use_bpe, threshold_pred_score, targeted=False) -> None:
        self.args = args
        self.model_sub = model_sub                        # substitute model (input: token_ids, output: embeddings)
        self.model_tgt = model_tgt                        # target model (input: tokens_ids, output: classify_logits)
        self.tokenizer = tokenizer                        # tokenizer of the substitute & target model
        self.model_mlm = model_mlm                        # no use here
        self.tokenizer_mlm = tokenizer_mlm                # used to convert the words into lowercase
        self.use_bpe = use_bpe                            # no use here
        self.threshold_pred_score = threshold_pred_score  # no use here
        self.iterations = 1
        self.targeted = targeted
    

    def loss(self, embedding_a, embedding_b):
        '''
        compute the squared distance between embedding_a and embedding_b
        '''        
        return nn.MSELoss()(embedding_a.to(self.args.device), embedding_b.to(self.args.device)).item()

    
    def compute_fitness(self, chromesome, codebert_tgt, tokenizer_tgt, orig_prob, orig_label, true_label ,code, names_positions_dict, args, orig_example=None, target_example=None):
        # 计算fitness function.
        # words + chromesome + orig_label + current_prob
        temp_code = map_chromesome(chromesome, code, "python")
        new_feature = self.convert_code_to_features(temp_code).input_ids
        new_embeddings = self.model_sub(torch.tensor(new_feature).unsqueeze(0).to(self.args.device))[0]
        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            fitness_value = -self.loss(target_embeddings, new_embeddings)
        else:
            orig_embeddings = self.model_sub(orig_example[0].unsqueeze(0).to(self.args.device))[0]
            fitness_value = self.loss(orig_embeddings, new_embeddings)
        return fitness_value


    def convert_code_to_features(self, code):
        code_tokens=self.tokenizer.tokenize(code)[:self.args.block_size-2]
        source_tokens =[self.tokenizer.cls_token]+code_tokens+[self.tokenizer.sep_token]
        source_ids =  self.tokenizer.convert_tokens_to_ids(source_tokens)
        padding_length = self.args.block_size - len(source_ids)
        source_ids+=[self.tokenizer.pad_token_id]*padding_length
        # print(source_ids) #[0, 49434, 49270, 35, 50118, 1437, 1437, 1437, 1437, 1437, 181, 18198, 219, 1577, 4, 17163, 28696, 1577, 12, 10799, 4, 179, 8061, 1577, 12, 10799, 4, 995, 50118, 1437, 50, 2128, 50118, 1437, 1437, 1437, 1437, 1437, 39825, 1577, 4, 17163, 28696, 1577, 12, 10799, 4, 179, 8061, 1577, 12, 10799, 4, 995, 50118, 1437, 49434, 50118, 1437, 1437, 50118, 1437, 3816, 11808, 1640, 179, 21710, 3256, 50118, 1437, 1437, 1437, 1437, 1437, 671, 8803, 43048, 50118, 1437, 1437, 50118, 1437, 3816, 10746, 1640, 21959, 11173, 6, 4047, 1848, 6, 230, 5214, 29802, 6, 13540, 47072, 3256, 50118, 1437, 1437, 1437, 1437, 1437, 221, 5457, 5456, 1640, 2544, 6, 4047, 1848, 4, 25616, 49123, 44154, 49338, 50118, 1437, 1437, 1437, 1437, 1437, 671, 8803, 43048, 50118, 1437, 1437, 50118, 1437, 3816, 9281, 2802, 1640, 21959, 11173, 6, 234, 5214, 29802, 6, 221, 5214, 29802, 6, 38, 5214, 29802, 6, 255, 5214, 29802, 6, 208, 5214, 29802, 6, 230, 5214, 29802, 6, 13540, 47072, 3256, 50118, 1437, 1437, 50118, 1437, 1437, 1437, 1437, 1437, 248, 6, 230, 6, 256, 5457, 221, 50118, 1437, 1437, 1437, 1437, 1437, 24537, 5457, 256, 50118, 1437, 1437, 50118, 1437, 1437, 1437, 1437, 1437, 274, 5457, 46446, 4, 30766, 48443, 48759, 955, 742, 1009, 230, 742, 1009, 248, 43, 50118, 1437, 1437, 1437, 1437, 1437, 150, 256, 8061, 321, 35, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 114, 248, 49095, 230, 8, 256, 49095, 230, 8, 248, 8061, 132, 35, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 256, 49826, 230, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 248, 49826, 112, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 274, 10975, 500, 742, 5457, 128, 3226, 108, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1615, 1594, 230, 8061, 248, 1437, 8, 256, 49095, 248, 8, 230, 8061, 132, 35, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 256, 49826, 248, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 230, 49826, 112, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 274, 10975, 46686, 230, 742, 5457, 128, 3226, 108, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1615, 1594, 248, 8061, 132, 8, 230, 8061, 132, 8, 36, 500, 8061, 155, 50, 230, 8061, 155, 50, 256, 45994, 112, 3256, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 114, 256, 28696, 230, 111, 112, 35, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 248, 49826, 112, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 274, 10975, 500, 6, 230, 111, 256, 35, 347, 742, 5457, 128, 3226, 108, 50118, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1437, 1615, 1594, 2]
        # print(len(source_ids)) #510
        return InputFeatures(source_tokens,source_ids, 0)



    def get_importance_score(self, code, words_list: list, sub_words: list, variable_names: list, model_type='classification', target_example=None):
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
            new_feature = self.convert_code_to_features(new_code)
            new_examples.append(new_feature.input_ids)
        # 3. 将他们转化成features
        embeddings_list = []
        for example in new_examples:
            # detach here is necessary to aviod OOM
            embeddings_list.append(self.model_sub(torch.tensor(example).unsqueeze(0).to(self.args.device))[0].detach().cpu())   
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
            new_feature = self.convert_code_to_features(new_code)
            new_feature.label = example[1].item()
            new_example.append(new_feature)
        new_dataset = CodeDataset(new_example)
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
        true_label = example[1].item()

        for k, _ in subs.items():
            if k in subs[k]:
                subs[k].remove(k)        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        identifiers, code_tokens = get_identifiers(code, 'python')
        prog_length = len(code_tokens)
        processed_code = " ".join(code_tokens)
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        variable_names = list(subs.keys())  # a list of all variables, including un-identifiers and identifiers

        if not orig_label == true_label:
            # 说明原来就是错的
            return None
        
        if len(variable_names) == 0:
            # 没有提取到identifier，直接退出
            print('Error! No variable_names extracted!')
            return None
        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]
        # 计算importance_score.
        # name_positions_dict: {key: identifier, value: a list records all the positions that the identifier occurs}
        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score_explain( 
                                                self.args, example, 
                                                processed_code,
                                                words,
                                                sub_words,
                                                variable_names,
                                                self.model_tgt, 
                                                self.tokenizer,
                                                [0,1], 
                                                batch_size=self.args.eval_batch_size, 
                                                max_length=self.args.block_size, 
                                                model_type='classification')
        

        if importance_score is None:
            print('Error! Importance_score is None!')
            return None
        # print(len(importance_score))
        # print(importance_score[0])
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
        print('greedy attack, self.args.num_of_changes: {}'.format(self.args.num_of_changes))

        # logits, preds, temp_loss = self.model_tgt.get_results([example], self.args.eval_batch_size)
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        orig_example = example
        orig_code = code
        adv_example = example
        adv_code = code
        orig_embeddings = self.model_sub(orig_example[0].unsqueeze(0).to(self.args.device))[0]


        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        orig_identifiers, orig_code_tokens = get_identifiers(orig_code, 'python') 
        orig_processed_code = " ".join(orig_code_tokens)
        # words: tokenized word from the code
        # sub_words: fine-grained words
        orig_words, orig_sub_words, orig_keys = _tokenize(orig_processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..


        adv_embeddings = self.model_sub(adv_example[0].unsqueeze(0).to(self.args.device))[0]
        for k, _ in subs.items():
            if k in subs[k]:
                subs[k].remove(k)

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = self.loss(orig_embeddings, adv_embeddings)


        # random initialization the adv_code
        replaced_words = {}
        identifiers, code_tokens = get_identifiers(adv_code, 'python') 
        print('num of identifiers: {}'.format(len(identifiers)))   # test
        used_substitutes = []
        for tgt_word in identifiers:
            tgt_word = tgt_word[0]
            all_substitutes = subs[tgt_word]
            for item in used_substitutes:
                if item in all_substitutes:
                    all_substitutes.remove(item)
            substitute = random.choice(all_substitutes)
            replaced_words[tgt_word] = substitute
            subs[substitute] = all_substitutes
            used_substitutes.append(substitute)
            adv_code = get_example(adv_code, tgt_word, substitute, 'python')
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        identifiers, code_tokens = get_identifiers(adv_code, 'python') 
        prog_length = len(code_tokens)

        processed_code = " ".join(code_tokens)
        adv_words, adv_sub_words, adv_keys = _tokenize(processed_code, self.tokenizer_mlm)
        
        # words: tokenized word from the code
        # sub_words: fine-grained words
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..


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

        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]

        # 计算importance_score.

        # name_positions_dict: {key: identifier, value: a list records all the positions that the identifier occurs}
        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score( 
                                                processed_code,
                                                adv_words,
                                                adv_sub_words,
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
                temp_code = get_example(adv_code, tgt_word, substitute, "python")
                                                
                new_feature = self.convert_code_to_features(temp_code)
                replace_examples.append(new_feature.input_ids)
            if len(replace_examples) == 0:
                # 并没有生成新的mutants，直接跳去下一个token
                continue

            replace_embeddings_list = []
            for example in replace_examples:
                replace_embeddings_list.append(self.model_sub(torch.tensor(example).unsqueeze(0).to(self.args.device))[0].detach().cpu())
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
                    adv_code = get_example(adv_code, tgt_word, candidate, "python")
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
                    adv_code = get_example(adv_code, tgt_word, candidate, "python")
                    replaced_words[tgt_word] = candidate
                    used_substitutes.append(candidate)
                    # print('word [{}] is removed from the all_substitutes list'.format(candidate))
                else:
                    replaced_words[tgt_word] = tgt_word
                    print('No Change! %s => %s', tgt_word, tgt_word)
            
            adv_code = adv_code
            if nb_changed_var >= self.args.num_of_changes:
                break

        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        adv_example = (torch.tensor(adv_feature.input_ids), true_label)

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words


    def greedy_attack_loss(self, example, code, subs, target_example=None):
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
            print('greedy attack, self.args.num_of_changes: {}'.format(self.args.num_of_changes))

            logits, preds, temp_loss = self.model_tgt.get_results([example], self.args.eval_batch_size)
            # logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
            orig_prob = logits[0]
            orig_label = preds[0]
            true_label = example[1].item()

            orig_example = example
            orig_code = code
            adv_example = example
            adv_code = code
            orig_embeddings = self.model_sub(orig_example[0].unsqueeze(0).to(self.args.device))[0]


            # identifier: the variable names that can be modified
            # code_tokens: tokenized code
            orig_identifiers, orig_code_tokens = get_identifiers(orig_code, 'python') 
            orig_processed_code = " ".join(orig_code_tokens)
            # words: tokenized word from the code
            # sub_words: fine-grained words
            orig_words, orig_sub_words, orig_keys = _tokenize(orig_processed_code, self.tokenizer_mlm)
            # 这里经过了小写处理..


            adv_embeddings = self.model_sub(adv_example[0].unsqueeze(0).to(self.args.device))[0]
            for k, _ in subs.items():
                if k in subs[k]:
                    subs[k].remove(k)

            if target_example is not None:
                target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
                assert orig_embeddings.shape == target_embeddings.shape
            
            if self.targeted:
                current_loss = self.loss(orig_embeddings, target_embeddings)
            else:
                current_loss = self.loss(orig_embeddings, adv_embeddings)


            # random initialization the adv_code
            replaced_words = {}
            identifiers, code_tokens = get_identifiers(adv_code, 'python') 
            print('num of identifiers: {}'.format(len(identifiers)))   # test
            used_substitutes = []
            for tgt_word in identifiers:
                tgt_word = tgt_word[0]
                all_substitutes = subs[tgt_word]
                for item in used_substitutes:
                    if item in all_substitutes:
                        all_substitutes.remove(item)
                substitute = random.choice(all_substitutes)
                replaced_words[tgt_word] = substitute
                subs[substitute] = all_substitutes
                used_substitutes.append(substitute)
                adv_code = get_example(adv_code, tgt_word, substitute, 'python')
            

            # identifier: the variable names that can be modified
            # code_tokens: tokenized code
            identifiers, code_tokens = get_identifiers(adv_code, 'python') 
            prog_length = len(code_tokens)

            processed_code = " ".join(code_tokens)
            adv_words, adv_sub_words, adv_keys = _tokenize(processed_code, self.tokenizer_mlm)
            
            # words: tokenized word from the code
            # sub_words: fine-grained words
            words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
            # 这里经过了小写处理..


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

            sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]

            # 计算importance_score.

            # name_positions_dict: {key: identifier, value: a list records all the positions that the identifier occurs}
            importance_score, replace_token_positions, names_positions_dict = self.get_importance_score( 
                                                    processed_code,
                                                    adv_words,
                                                    adv_sub_words,
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
                    temp_code = get_example(adv_code, tgt_word, substitute, "python")
                                                    
                    new_feature = self.convert_code_to_features(temp_code)
                    replace_examples.append(new_feature.input_ids)
                if len(replace_examples) == 0:
                    # 并没有生成新的mutants，直接跳去下一个token
                    continue

                replace_embeddings_list = []
                for example in replace_examples:
                    replace_embeddings_list.append(self.model_sub(torch.tensor(example).unsqueeze(0).to(self.args.device))[0].detach().cpu())
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
                        adv_code = get_example(adv_code, tgt_word, candidate, "python")
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
                        adv_code = get_example(adv_code, tgt_word, candidate, "python")
                        replaced_words[tgt_word] = candidate
                        used_substitutes.append(candidate)
                        # print('word [{}] is removed from the all_substitutes list'.format(candidate))
                    else:
                        replaced_words[tgt_word] = tgt_word
                        print('No Change! %s => %s', tgt_word, tgt_word)
                
                adv_code = adv_code
                if nb_changed_var >= self.args.num_of_changes:
                    break

            #  query the model_tgt to see whether the attack is success
            adv_feature = self.convert_code_to_features(adv_code)
            adv_feature.label = 0    # set a pseduo label
            adv_dataset = CodeDataset([adv_feature])
            logits, preds, tgt_model_loss = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
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

            adv_example = (torch.tensor(adv_feature.input_ids), true_label)
            sub_model_loss = current_loss

            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words, sub_model_loss, tgt_model_loss



    def beam_attack(self, example, code, subs, num_beam=3, target_example=None):
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

        for k, v in subs.items():
            print('length of substitutes for each target word: {}'.format(len(v)))
            break

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        orig_example = example
        orig_code = code
        adv_example = example
        adv_code = code
        orig_embeddings = self.model_sub(orig_example[0].unsqueeze(0).to(self.args.device))[0]


        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        orig_identifiers, orig_code_tokens = get_identifiers(orig_code, 'python') 
        orig_processed_code = " ".join(orig_code_tokens)
        # words: tokenized word from the code
        # sub_words: fine-grained words
        orig_words, orig_sub_words, orig_keys = _tokenize(orig_processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..

        adv_embeddings = self.model_sub(adv_example[0].unsqueeze(0).to(self.args.device))[0]
        temp_subs = copy.deepcopy(subs)
        for k, _ in temp_subs.items():
            if k in temp_subs[k]:
                temp_subs[k].remove(k)

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = self.loss(orig_embeddings, adv_embeddings)


        # # random initialization the adv_code
        # replaced_words = {}
        # identifiers, code_tokens = get_identifiers(adv_code, 'python') 
        # used_substitutes = []
        # for tgt_word in identifiers:
        #     tgt_word = tgt_word[0]
        #     all_substitutes = subs[tgt_word]
        #     for item in used_substitutes:
        #         if item in all_substitutes:
        #             all_substitutes.remove(item)
        #     substitute = random.choice(all_substitutes)
        #     replaced_words[tgt_word] = substitute
        #     subs[substitute] = all_substitutes
        #     used_substitutes.append(substitute)
        #     adv_code = get_example(adv_code, tgt_word, substitute, 'python')
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        identifiers, code_tokens = get_identifiers(adv_code, 'python') 
        prog_length = len(code_tokens)

        processed_code = " ".join(code_tokens)
        
        # words: tokenized word from the code
        # sub_words: fine-grained words
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..


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

        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]

        # 计算importance_score.

        # name_positions_dict: {key: identifier, value: a list records all the positions that the identifier occurs}
        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score(orig_example, 
                                                processed_code,
                                                orig_words,
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

        final_code = copy.deepcopy(adv_code)
        nb_changed_var = 0 # 表示被修改的variable数量
        nb_changed_pos = 0
        is_success = -1
        
        # initialize
        beam_search_candidates = []
        for _ in range(num_beam):
            beam_search_candidates.append({'code': final_code, 'used_substitutes': [], 'replaced_words': {}, 'score': 0.0})


        for name_and_score in sorted_list_of_names:
            # generated new candidates for each step and add them into the candidate set
            for current_beam in beam_search_candidates:
                tgt_word = name_and_score[0]
                all_substitutes = temp_subs[tgt_word]
                # delete used substitutes
                for item in current_beam['used_substitutes']:
                    if item in all_substitutes:
                        all_substitutes.remove(item)

                best_loss = math.inf if self.targeted else 0.0
                candidate = None
                replace_examples = []

                for substitute in all_substitutes:

                    # 需要将几个位置都替换成sustitue_
                    temp_code = get_example(current_beam['code'], tgt_word, substitute, "python")
                    if temp_code not in [item['code'] for item in beam_search_candidates]:
                        # make sure that there is no repeated beams
                        temp_used_substitutes = copy.deepcopy(current_beam['used_substitutes'])
                        temp_used_substitutes.append(substitute)
                                                        
                        new_feature = self.convert_code_to_features(temp_code).input_ids
                        temp_embedding = self.model_sub(torch.tensor(new_feature).unsqueeze(0).to(self.args.device))[0].detach()
                        temp_score = self.loss(temp_embedding, target_embeddings) if self.targeted else self.loss(temp_embedding, orig_embeddings)
                        temp_replaced_words = copy.deepcopy(current_beam['replaced_words'])
                        temp_replaced_words[tgt_word] = substitute
                        beam_search_candidates.append({'code': temp_code, 'used_substitutes': temp_used_substitutes, 'replaced_words': temp_replaced_words, 'score': temp_score})
            # tackle the situation where there is no changes in this step
            for i in range(num_beam):
                beam_search_candidates[i]['replaced_words'][tgt_word] = tgt_word
            # sort all candidates in terms of score and save only num_beam candidates  
            sorted_beam = sorted(beam_search_candidates, key=lambda x: x['score'], reverse=True)
            beam_search_candidates = sorted_beam[:num_beam]         

            print('--------------------------------------------')
            for index, beam in enumerate(beam_search_candidates):
                print('Selected Beam %d: %s => %s, score = %.5f' % (index, tgt_word, beam['used_substitutes'][-1], beam['score']), flush=True)
                
        adv_code = beam_search_candidates[0]['code']
        replaced_words = beam_search_candidates[0]['replaced_words']

        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        adv_example = (torch.tensor(adv_feature.input_ids), true_label)

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



    def beam_attack_random_start(self, example, code, subs, num_beam=3, target_example=None):

        def random_init(adv_code, subs):
            # random initialization the adv_code
            replaced_words = {}
            identifiers, code_tokens = get_identifiers(adv_code, 'python') 
            used_substitutes = []
            for tgt_word in identifiers:
                tgt_word = tgt_word[0]
                all_substitutes = subs[tgt_word]
                for item in used_substitutes:
                    if item in all_substitutes:
                        all_substitutes.remove(item)
                substitute = random.choice(all_substitutes)
                replaced_words[tgt_word] = substitute
                subs[substitute] = all_substitutes
                used_substitutes.append(substitute)
                adv_code = get_example(adv_code, tgt_word, substitute, 'python')
            return adv_code, subs, replaced_words

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


        for k, v in subs.items():
            print('length of substitutes for each target word: {}'.format(len(v)))
            break

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        orig_example = example
        orig_code = code
        adv_example = example
        adv_code = code
        orig_embeddings = self.model_sub(orig_example[0].unsqueeze(0).to(self.args.device))[0]

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        orig_identifiers, orig_code_tokens = get_identifiers(orig_code, 'python') 
        orig_processed_code = " ".join(orig_code_tokens)
        # words: tokenized word from the code
        # sub_words: fine-grained words
        orig_words, orig_sub_words, orig_keys = _tokenize(orig_processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..

        adv_embeddings = self.model_sub(adv_example[0].unsqueeze(0).to(self.args.device))[0]
        temp_subs = copy.deepcopy(subs)
        for k, _ in temp_subs.items():
            if k in temp_subs[k]:
                temp_subs[k].remove(k)

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = self.loss(orig_embeddings, adv_embeddings)
        
        # random initialization
        beam_search_candidates = []
        for _ in range(num_beam):
            candidate = {}
            adv_code, temp_subs, replaced_words = random_init(code, temp_subs)
            candidate['code'] = adv_code

            # identifier: the variable names that can be modified
            # code_tokens: tokenized code
            identifiers, code_tokens = get_identifiers(adv_code, 'python') 
            prog_length = len(code_tokens)

            processed_code = " ".join(code_tokens)
            
            # words: tokenized word from the code
            # sub_words: fine-grained words
            words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
            # 这里经过了小写处理..


            variable_names = list(temp_subs.keys())  # a list of all variables, including un-identifiers and identifiers
            
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

            sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]

            # 计算importance_score.
            # name_positions_dict: {key: identifier, value: a list records all the positions that the identifier occurs}
            importance_score, replace_token_positions, names_positions_dict = self.get_importance_score(
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

            candidate['sorted_list_of_names'] = sorted_list_of_names
            candidate['used_substitutes'] = []
            candidate['replaced_words'] = replaced_words
            candidate['score'] = 0.0
            beam_search_candidates.append(candidate)



        final_code = copy.deepcopy(adv_code)
        nb_changed_var = 0 # 表示被修改的variable数量
        nb_changed_pos = 0
        is_success = -1


        for i in range(len(beam_search_candidates[0]['sorted_list_of_names'])):
            for j in range(num_beam):
                current_beam = beam_search_candidates[j]
                name_and_score = current_beam['sorted_list_of_names'][i]
                tgt_word = name_and_score[0]
                all_substitutes = temp_subs[tgt_word]
                # delete used substitutes
                for item in current_beam['used_substitutes']:
                    if item in all_substitutes:
                        all_substitutes.remove(item)

                best_loss = math.inf if self.targeted else 0.0
                candidate = None
                replace_examples = []

                for substitute in all_substitutes:

                    # 需要将几个位置都替换成sustitue_
                    temp_code = get_example(current_beam['code'], tgt_word, substitute, "python")
                    if temp_code not in [item['code'] for item in beam_search_candidates]:
                        # make sure that there is no repeated beams
                        temp_used_substitutes = copy.deepcopy(current_beam['used_substitutes'])
                        temp_used_substitutes.append(substitute)
                                                        
                        new_feature = self.convert_code_to_features(temp_code).input_ids
                        temp_embedding = self.model_sub(torch.tensor(new_feature).unsqueeze(0).to(self.args.device))[0].detach()
                        temp_score = self.loss(temp_embedding, target_embeddings) if self.targeted else self.loss(temp_embedding, orig_embeddings)
                        temp_replaced_words = copy.deepcopy(current_beam['replaced_words'])
                        temp_replaced_words[tgt_word] = substitute
                        beam_search_candidates.append({'code': temp_code, 'used_substitutes': temp_used_substitutes, 'replaced_words': temp_replaced_words, 'score': temp_score, 'sorted_list_of_names': current_beam['sorted_list_of_names']})
            # tackle the situation where there is no changes in this step
            for i in range(num_beam):
                beam_search_candidates[i]['replaced_words'][tgt_word] = tgt_word
            # sort all candidates in terms of score and save only num_beam candidates  
            sorted_beam = sorted(beam_search_candidates, key=lambda x: x['score'], reverse=True)
            beam_search_candidates = sorted_beam[:num_beam]         

            print('--------------------------------------------')
            for index, beam in enumerate(beam_search_candidates):
                print('Selected Beam %d: %s => %s, score = %.5f' % (index, tgt_word, beam['used_substitutes'][-1], beam['score']), flush=True)
                
        adv_code = beam_search_candidates[0]['code']
        replaced_words = beam_search_candidates[0]['replaced_words']

        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        adv_example = (torch.tensor(adv_feature.input_ids), true_label)

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



    def ga_attack(self, example, code, subs, initial_replace=None, target_example=None):
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


        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1]

        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        # logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            print('orig_embeddings.shape: {}, target_embeddings.shape: {}'.format(orig_embeddings.shape, target_embeddings.shape))
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0

        adv_code = code

        temp_label = None

        identifiers, code_tokens = get_identifiers(code, 'python')
        prog_length = len(code_tokens)


        processed_code = " ".join(code_tokens)
        
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..


        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None
            
        if len(variable_names) == 0:
            # 没有提取到identifier，直接退出
            is_success = -3
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        names_positions_dict = get_identifier_posistions_from_code(words, variable_names)

        nb_changed_var = 0 # 表示被修改的variable数量
        nb_changed_pos = 0
        is_success = -1

        # 我们可以先生成所有的substitutes
        variable_substitute_dict = {}

        for tgt_word in names_positions_dict.keys():
            variable_substitute_dict[tgt_word] = subs[tgt_word]

        fitness_values = []
        base_chromesome = {word: word for word in variable_substitute_dict.keys()}
        population = [base_chromesome]
        # 关于chromesome的定义: {tgt_word: candidate, tgt_word_2: candidate_2, ...}
        for tgt_word in variable_substitute_dict.keys():
            # 这里进行初始化
            if initial_replace is None:
                # 对于每个variable: 选择"影响最大"的substitutes
                replace_examples = []
                substitute_list = []
                
                best_loss = math.inf if self.targeted else 0.0
                initial_candidate = tgt_word
                tgt_positions = names_positions_dict[tgt_word]
                
                # 原来是随机选择的，现在要找到改变最大的.
                for a_substitute in variable_substitute_dict[tgt_word]:
                    # a_substitute = a_substitute.strip()
                    
                    substitute_list.append(a_substitute)
                    # 记录下这次换的是哪个substitute
                    temp_code = get_example(code, tgt_word, a_substitute, "python") 
                    new_feature = self.convert_code_to_features(temp_code)
                    replace_examples.append(new_feature.input_ids)

                if len(replace_examples) == 0:
                    # 并没有生成新的mutants，直接跳去下一个token
                    continue

                replace_embeddings_list = []
                for example in replace_examples:
                    replace_embeddings_list.append(self.model_sub(torch.tensor(example).unsqueeze(0).to(self.args.device))[0].detach().cpu())
                    # 3. 将他们转化成features
                replace_embeddings = torch.stack(replace_embeddings_list)

                _the_best_candidate = -1
                if self.targeted:
                    for index, embed in enumerate(replace_embeddings):
                        loss = self.loss(embed, target_embeddings)
                        if loss < best_loss:
                            best_loss = loss
                            _the_best_candidate = index
                else:
                    for index, embed in enumerate(replace_embeddings):
                        loss = self.loss(embed, orig_embeddings)
                        if loss > best_loss:
                            best_loss = loss
                            _the_best_candidate = index
                if _the_best_candidate == -1:
                    initial_candidate = tgt_word
                else:
                    initial_candidate = substitute_list[_the_best_candidate]
            else:
                try:
                    initial_candidate = initial_replace[tgt_word]
                except:
                    initial_candidate = tgt_word

            temp_chromesome = copy.deepcopy(base_chromesome)
            temp_chromesome[tgt_word] = initial_candidate
            population.append(temp_chromesome)
            if target_example is not None:
                temp_fitness = self.compute_fitness(temp_chromesome, self.model_tgt, self.tokenizer, max(orig_prob), orig_label, true_label ,code, names_positions_dict, self.args, orig_example=example, target_example=target_example)
            else:
                temp_fitness = self.compute_fitness(temp_chromesome, self.model_tgt, self.tokenizer, max(orig_prob), orig_label, true_label ,code, names_positions_dict, self.args, orig_example=example, target_example=None)
            fitness_values.append(temp_fitness)

        cross_probability = 0.7

        max_iter = max(5 * len(population), 10)
        # 这里的超参数还是得调试一下.

        for i in range(max_iter):
            _temp_mutants = []
            for j in range(self.args.eval_batch_size):
                p = random.random()
                chromesome_1, index_1, chromesome_2, index_2 = select_parents(population)
                if p < cross_probability: # 进行crossover
                    if chromesome_1 == chromesome_2:
                        child_1 = mutate(chromesome_1, variable_substitute_dict)
                        continue
                    child_1, child_2 = crossover(chromesome_1, chromesome_2)
                    if child_1 == chromesome_1 or child_1 == chromesome_2:
                        child_1 = mutate(chromesome_1, variable_substitute_dict)
                else: # 进行mutates
                    child_1 = mutate(chromesome_1, variable_substitute_dict)
                _temp_mutants.append(child_1)
            
            # compute fitness in batch
            feature_list = []
            for mutant in _temp_mutants:
                _temp_code = map_chromesome(mutant, code, "python")
                _tmp_feature = self.convert_code_to_features(_temp_code)
                feature_list.append(_tmp_feature.input_ids)
            if len(feature_list) == 0:
                continue
            # mutate_logits, mutate_preds = self.model_tgt.get_results(new_dataset, self.args.eval_batch_size)
            mutate_embeddings_list = []
            for feature in feature_list:
                mutate_embeddings_list.append(self.model_sub(torch.tensor(feature).unsqueeze(0).to(self.args.device))[0].detach().cpu())
            mutate_embeddings = torch.stack(mutate_embeddings_list)
            mutate_fitness_values = []
            for index, mutate_embed in enumerate(mutate_embeddings):
                if self.targeted:
                    _tmp_fitness = -self.loss(mutate_embed, target_embeddings)
                    mutate_fitness_values.append(_tmp_fitness)
                else:
                    _tmp_fitness = self.loss(mutate_embed, orig_embeddings)
                    mutate_fitness_values.append(_tmp_fitness)
                
            # 现在进行替换.
            for index, fitness_value in enumerate(mutate_fitness_values):
                min_value = min(fitness_values)
                if fitness_value > min_value:
                    # 替换.
                    min_index = fitness_values.index(min_value)
                    population[min_index] = _temp_mutants[index]
                    fitness_values[min_index] = fitness_value

        best_index = 0
        best_fitness = 0
        for index, fitness_value in enumerate(fitness_values):
            if fitness_value > best_fitness:
                best_index = index
                best_fitness = fitness_value

        adv_code = map_chromesome(population[best_index], code, "python")
        for old_word in population[best_index].keys():
            if old_word == population[index][old_word]:
                nb_changed_var += 1
                nb_changed_pos += len(names_positions_dict[old_word])

        
        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('GA Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('GA Attack Success!!!')
            else:
                is_success = -1

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, nb_changed_var, nb_changed_pos, None
    

    def greedy_attack_baseline(self, example, code, subs, target_example=None):
        '''
        Params
        example: tuple, size=2, [0] is input example (tensor, shape=(1, 510)), [1] is its true label (tensor)
        code: input code in string format
        subs: dict, key: the variable name in input code; value: the candidate substitute variable list
        target_example: same as 'example'
        '''
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
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        identifiers, code_tokens = get_identifiers(code, 'python') 
        prog_length = len(code_tokens)

        processed_code = " ".join(code_tokens)

        # words: tokenized word from the code
        # sub_words: fine-grained words
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..


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

        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]

        # 计算importance_score.

        # name_positions_dict: {key: identifier, value: a list records all the positions that the identifier occurs}
        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score(
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

        final_code = copy.deepcopy(code)
        nb_changed_var = 0 # 表示被修改的variable数量
        nb_changed_pos = 0
        is_success = -1
        replaced_words = {}

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
            # 依次记录了被加进来的substitute
            # 即，每个temp_replace对应的substitute.
            for substitute in all_substitutes:
                
                substitute_list.append(substitute)
                # 记录了替换的顺序

                # 需要将几个位置都替换成sustitue_
                temp_code = get_example(final_code, tgt_word, substitute, "python")
                                                
                new_feature = self.convert_code_to_features(temp_code)
                replace_examples.append(new_feature.input_ids)
            if len(replace_examples) == 0:
                # 并没有生成新的mutants，直接跳去下一个token
                continue

            replace_embeddings_list = []
            for example in replace_examples:
                replace_embeddings_list.append(self.model_sub(torch.tensor(example).unsqueeze(0).to(self.args.device))[0].detach().cpu())
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
                    final_code = get_example(final_code, tgt_word, candidate, "python")
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
                    final_code = get_example(final_code, tgt_word, candidate, "python")
                    replaced_words[tgt_word] = candidate
                    used_substitutes.append(candidate)
                    # print('word [{}] is removed from the all_substitutes list'.format(candidate))
                else:
                    replaced_words[tgt_word] = tgt_word
            
            adv_code = final_code


        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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




    def insert_attack(self, example, code, subs, target_example=None):
        '''
        Params
        example: tuple, size=2, [0] is input example (tensor, shape=(1, 510)), [1] is its true label (tensor)
        code: input code in string format
        subs: dict, key: the variable name in input code; value: the candidate substitute variable list
        target_example: same as 'example'
        '''
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


        def get_insert_masked_code(code, pos):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
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

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + variable_statement)
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        # identifiers, code_tokens = get_identifiers(code, 'python') 
        # print(identifiers)
        # prog_length = len(code_tokens)
        prog_length = 0

        # processed_code = " ".join(code_tokens)

        # print('adv_code: {}'.format(adv_code))   # test

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall('\n', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            processed_masked_code = ' ' + masked_code
            masked_feature = self.convert_code_to_features(processed_masked_code).input_ids
            masked_embeddings = self.model_sub(torch.tensor(masked_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        for k, v in subs.items():
            subs_for_insert = v
            break

        #剔除原代码中的变量名
        # subs_var = subs_for_insert
        # for used_var in identifiers:
        #     used_var = used_var[0]
        #     if used_var in subs_var:
        #         subs_var.remove(used_var)

        print('Insertable num: ', len(sorted_id))
        inserted_num = 0
        for i, insert_idx in enumerate(sorted_id):
            # print('i = {}, pos = {}'.format(i, insert_idx))
            # print('code lines: ', len(final_code.split('\n')))
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, insert_idx, 'temp_variable = ' + "'" + str(sub) + "'")
                processed_adv_code = ' ' + adv_code
                adv_feature = self.convert_code_to_features(processed_adv_code).input_ids
                adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
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
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = [], {}, 0, {}

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words


    def empty_print_attack(self, example, code, subs, target_example=None):
        '''
        Params
        example: tuple, size=2, [0] is input example (tensor, shape=(1, 510)), [1] is its true label (tensor)
        code: input code in string format
        subs: dict, key: the variable name in input code; value: the candidate substitute variable list
        target_example: same as 'example'
        '''
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


        def get_insert_masked_code(code, pos):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str


        def get_inserted_code(code, pos, variable_statement="print('', end='')"):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + variable_statement)
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        # identifiers, code_tokens = get_identifiers(code, 'python') 
        # print(identifiers)
        # prog_length = len(code_tokens)
        prog_length = 0

        # processed_code = " ".join(code_tokens)

        # print('adv_code: {}'.format(adv_code))   # test

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        insert_pos_nums = len(re.findall('\n', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            processed_masked_code = ' ' + masked_code
            masked_feature = self.convert_code_to_features(processed_masked_code).input_ids
            masked_embeddings = self.model_sub(torch.tensor(masked_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        for i, inserted_id in enumerate(sorted_id):
            if i >= self.args.num_of_changes:
                break
            update_flag = False
            adv_code = get_inserted_code(final_code, inserted_id)
            processed_adv_code = ' ' + adv_code
            adv_feature = self.convert_code_to_features(processed_adv_code).input_ids
            adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
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

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = [], {}, 0, {}

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words




    def nonreachable_if_attack(self, example, code, subs, target_example=None):
        '''
        Params
        example: tuple, size=2, [0] is input example (tensor, shape=(1, 510)), [1] is its true label (tensor)
        code: input code in string format
        subs: dict, key: the variable name in input code; value: the candidate substitute variable list
        target_example: same as 'example'
        '''
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


        def get_insert_masked_code(code, pos):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str


        def get_inserted_code(code, pos, print_statement):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + 'if False:\n' + ' ' * (space_num + 4) + 'print("{}")'.format(print_statement))
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        # identifiers, code_tokens = get_identifiers(code, 'python') 
        # print(identifiers)
        # prog_length = len(code_tokens)
        prog_length = 0

        # processed_code = " ".join(code_tokens)

        # print('adv_code: {}'.format(adv_code))   # test

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, orig_label, temp_label, None, []

        insert_pos_nums = len(re.findall('\n', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            processed_masked_code = ' ' + masked_code
            masked_feature = self.convert_code_to_features(processed_masked_code).input_ids
            masked_embeddings = self.model_sub(torch.tensor(masked_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        for k, v in subs.items():
            subs_for_insert = v
            break

        inserted_num = 0
        for i, inserted_id in enumerate(sorted_id):
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, inserted_id, str(sub))
                processed_adv_code = ' ' + adv_code
                adv_feature = self.convert_code_to_features(processed_adv_code).input_ids
                adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
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
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = [], {}, 0, {}

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



    def nonreachable_while_attack(self, example, code, subs, target_example=None):
        '''
        Params
        example: tuple, size=2, [0] is input example (tensor, shape=(1, 510)), [1] is its true label (tensor)
        code: input code in string format
        subs: dict, key: the variable name in input code; value: the candidate substitute variable list
        target_example: same as 'example'
        '''
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


        def get_insert_masked_code(code, pos):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str


        def get_inserted_code(code, pos, print_statement):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + 'while False:\n' + ' ' * (space_num + 4) + 'print("{}")'.format(print_statement))
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        # print(example[0])
        # print(example[0].shape) #torch.Size([510])
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        # identifiers, code_tokens = get_identifiers(code, 'python') 
        # print(identifiers)
        # prog_length = len(code_tokens)
        prog_length = 0

        # processed_code = " ".join(code_tokens)

        # print('adv_code: {}'.format(adv_code))   # test

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        insert_pos_nums = len(re.findall('\n', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            processed_masked_code = ' ' + masked_code
            masked_feature = self.convert_code_to_features(processed_masked_code).input_ids
            masked_embeddings = self.model_sub(torch.tensor(masked_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        for k, v in subs.items():
            subs_for_insert = v
            break

        for i, inserted_id in enumerate(sorted_id):
            if i >= self.args.num_of_changes:
                break
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, inserted_id, str(sub))
                processed_adv_code = ' ' + adv_code
                adv_feature = self.convert_code_to_features(processed_adv_code).input_ids
                adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
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

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = [], {}, 0, {}

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



    def unused_classmember_attack(self, example, code, subs, target_example=None):
        '''
        Params
        example: tuple, size=2, [0] is input example (tensor, shape=(1, 510)), [1] is its true label (tensor)
        code: input code in string format
        subs: dict, key: the variable name in input code; value: the candidate substitute variable list
        target_example: same as 'example'
        '''
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
        
        def is_init_declaration(code, pos):
            '''
            判断pos行是否可以插入self.temp_variable = 'XXX'
            在整个攻击代码逻辑中，pos表示的是在原始代码的第pos行的前面将要插入新的一行，
            因此应该确保pos行的前一行(pos-1)包含'def __init__(*self*):'
            '''
            import re
            if pos <= 0:
                return False, False
            else:
                insert_pos = pos
                init_declaration_pos = pos - 1
                splited_code = code.split('\n')
                member = True if re.match(pattern=r".*def.*\(.*self.*\).*:.*", 
                                     string=splited_code[init_declaration_pos]) else False
                function = True if re.match(pattern=r".*def.*\(.*\).*:.*", 
                                    string=splited_code[init_declaration_pos]) else False
                if member or function:   # test
                    print('match success at {}'.format(splited_code[init_declaration_pos]))
                else:
                    print('match false at {}'.format(splited_code[init_declaration_pos]))
                return member, function



        def get_insert_masked_code(code, pos):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
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

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + variable_statement)
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        # identifiers, code_tokens = get_identifiers(code, 'python') 
        # print(identifiers)
        # prog_length = len(code_tokens)
        prog_length = 0

        # processed_code = " ".join(code_tokens)

        # print('adv_code: {}'.format(adv_code))   # test

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall('\n', adv_code))
        importance_score = []

        init_exist_flag = False
        for i in range(insert_pos_nums):
            member, function = is_init_declaration(adv_code, i)
            if member or function:
                masked_code = get_insert_masked_code(adv_code, i)
                processed_masked_code = ' ' + masked_code
                masked_feature = self.convert_code_to_features(processed_masked_code).input_ids
                masked_embeddings = self.model_sub(torch.tensor(masked_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
                importance_score.append(self.loss(orig_embeddings, masked_embeddings))
                init_exist_flag = True
            else:
                importance_score.append(0.0)
        
        if init_exist_flag == False:
            is_success = -1
            temp_label = orig_label
            print('**********No __init__ declaration in this code, attack failed**********')
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = copy.deepcopy(code)

        for k, v in subs.items():
            subs_for_insert = v
            break

        #剔除原代码中的变量名
        # subs_var = subs_for_insert
        # for used_var in identifiers:
        #     used_var = used_var[0]
        #     if used_var in subs_var:
        #         subs_var.remove(used_var)

        print('Insertable num: ', len(sorted_id))
        inserted_num = 0
        for i, insert_idx in enumerate(sorted_id):
            member, function = is_init_declaration(adv_code, insert_idx)
            if member or function:
                update_flag = False
                while True:
                    for sub in subs_for_insert:
                        insert_string = 'self.temp_variable{} = '.format(inserted_num) + "'" + str(sub) + "'" if member else 'temp_variable{} = '.format(inserted_num) + "'" + str(sub) + "'"
                        temp_code = get_inserted_code(adv_code, insert_idx, insert_string)
                        processed_temp_code = ' ' + temp_code
                        adv_feature = self.convert_code_to_features(processed_temp_code).input_ids
                        adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
                        loss_value = self.loss(orig_embeddings, adv_embeddings)
                        if loss_value > temp_best_loss:
                            temp_best_loss = loss_value
                            temp_best_code = temp_code
                            update_flag = True

                    adv_code = temp_best_code

                    print('Loss value increased: current loss = {}'.format(temp_best_loss))
                    
                    if update_flag:
                        for idx in range(len(sorted_id)):
                            if sorted_id[idx] >= insert_idx:
                                sorted_id[idx] += 1
                        inserted_num += 1
                    #控制插入数量
                    if inserted_num >= self.args.num_of_changes:
                        break 

        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        print('success: {}, adv_code: {}'.format(is_success, adv_code))

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = [], {}, 0, {}

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words

    
    def insert_comments_attack(self, example, code, subs, target_example=None):
        '''
        Params
        example: tuple, size=2, [0] is input example (tensor, shape=(1, 510)), [1] is its true label (tensor)
        code: input code in string format
        subs: dict, key: the variable name in input code; value: the candidate substitute variable list
        target_example: same as 'example'
        '''
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


        def get_insert_masked_code(code, pos):
            def count_space(line):
                count = 0
                for char in line:
                    if char == ' ':
                        count += 1
                    if char != ' ':
                        break
                return count

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
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

            splited_code = code.split('\n')
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + variable_statement)
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        # identifiers, code_tokens = get_identifiers(code, 'python') 
        # print(identifiers)
        # prog_length = len(code_tokens)
        prog_length = 0

        # processed_code = " ".join(code_tokens)

        # print('adv_code: {}'.format(adv_code))   # test

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall('\n', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            processed_masked_code = ' ' + masked_code
            masked_feature = self.convert_code_to_features(processed_masked_code).input_ids
            masked_embeddings = self.model_sub(torch.tensor(masked_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        final_code = copy.deepcopy(code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        for k, v in subs.items():
            subs_for_insert = v
            break

        #剔除原代码中的变量名
        # subs_var = subs_for_insert
        # for used_var in identifiers:
        #     used_var = used_var[0]
        #     if used_var in subs_var:
        #         subs_var.remove(used_var)

        print('Insertable num: ', len(sorted_id))
        inserted_num = 0
        for i, insert_idx in enumerate(sorted_id):
            # print('i = {}, pos = {}'.format(i, insert_idx))
            # print('code lines: ', len(final_code.split('\n')))
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, insert_idx, '# ' + str(sub))
                processed_adv_code = ' ' + adv_code
                adv_feature = self.convert_code_to_features(processed_adv_code).input_ids
                adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
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
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('Insert_comments Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('Insert_comments Attack Success!!!')
            else:
                is_success = -1

        print('success: {}, adv_code: {}'.format(is_success, final_code))

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = [], {}, 0, {}

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words


    def unused_function_arguments_attack(self, example, code, subs, target_example=None):
        '''
        Params
        example: tuple, size=2, [0] is input example (tensor, shape=(1, 510)), [1] is its true label (tensor)
        code: input code in string format
        subs: dict, key: the variable name in input code; value: the candidate substitute variable list
        target_example: same as 'example'
        '''
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
        
        def is_function_declaration(code, pos):
            '''
            判断pos行是否可以插入temp_variable='XXX'
            在整个攻击代码逻辑中, pos表示的是在原始代码的第pos行的前面将要插入新的一行,
            因此应该确保pos行的前一行(pos-1)包含'def __init__(*self*):'
            '''
            import re
            if pos <= 0:
                return False
            else:
                insert_pos = pos
                function_declaration_pos = pos - 1
                splited_code = code.split('\n')
                function = True if re.match(pattern=r".*def.*\(.*\).*:.*", 
                                    string=splited_code[function_declaration_pos]) else False
                if function:   # test
                    print('match success at {}'.format(splited_code[function_declaration_pos]))
                else:
                    print('match false at {}'.format(splited_code[function_declaration_pos]))
                return function



        def get_insert_masked_code(code, pos):
            splited_code = code.split('\n')
            temp_line = splited_code[pos-1]
            start_idx = temp_line.find('def')
            end_idx = temp_line.find(')', start_idx)
            # print(temp_line)
            # print('start_idx: ', start_idx)
            # print('end_idx: ', end_idx)
            if temp_line[end_idx-1] != '(':
                splited_code[pos-1] = temp_line[:end_idx] + ', <mask>' + code[end_idx:]
            else:
                splited_code[pos-1] = temp_line[:end_idx] + '<mask>' + code[end_idx:]

            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str


        def get_inserted_code(code, pos, variable_statement):
            splited_code = code.split('\n')
            temp_line = splited_code[pos-1]
            start_idx = temp_line.find('def')
            end_idx = temp_line.find(')', start_idx)
            if temp_line[end_idx-1] != '(':
                splited_code[pos-1] = temp_line[:end_idx] + ', ' + variable_statement + code[end_idx:]
            else:
                splited_code[pos-1] = temp_line[:end_idx] + variable_statement + code[end_idx:]
            
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.model_sub(example[0].unsqueeze(0).to(self.args.device))[0]
        

        if target_example is not None:
            target_embeddings = self.model_sub(target_example[0].unsqueeze(0).to(self.args.device))[0]
            assert orig_embeddings.shape == target_embeddings.shape
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        

        # identifier: the variable names that can be modified
        # code_tokens: tokenized code
        # identifiers, code_tokens = get_identifiers(code, 'python') 
        # print(identifiers)
        # prog_length = len(code_tokens)
        prog_length = 0

        # processed_code = " ".join(code_tokens)

        # print('adv_code: {}'.format(adv_code))   # test

        variable_names = list(subs.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            temp_label = orig_label
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall('\n', adv_code))
        importance_score = []

        init_exist_flag = False
        for i in range(insert_pos_nums):
            function = is_function_declaration(adv_code, i)
            if function:
                masked_code = get_insert_masked_code(adv_code, i)
                processed_masked_code = ' ' + masked_code
                masked_feature = self.convert_code_to_features(processed_masked_code).input_ids
                masked_embeddings = self.model_sub(torch.tensor(masked_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
                importance_score.append(self.loss(orig_embeddings, masked_embeddings))
                init_exist_flag = True
            else:
                importance_score.append(0.0)
        
        if init_exist_flag == False:
            is_success = -1
            temp_label = orig_label
            print('**********No function declaration in this code, attack failed**********')
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])

        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = copy.deepcopy(code)

        for k, v in subs.items():
            subs_for_insert = v
            break

        #剔除原代码中的变量名
        # subs_var = subs_for_insert
        # for used_var in identifiers:
        #     used_var = used_var[0]
        #     if used_var in subs_var:
        #         subs_var.remove(used_var)

        print('Insertable num: ', len(sorted_id))
        inserted_num = 0
        for i, insert_idx in enumerate(sorted_id):
            function = is_function_declaration(adv_code, insert_idx)
            if function:
                update_flag = False
                while True:
                    for sub in subs_for_insert:
                        insert_string = 'temp_variable{}='.format(inserted_num) + "'" + str(sub) + "'"
                        temp_code = get_inserted_code(adv_code, insert_idx, insert_string)
                        processed_temp_code = ' ' + temp_code
                        adv_feature = self.convert_code_to_features(processed_temp_code).input_ids
                        adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0].detach().cpu()
                        loss_value = self.loss(orig_embeddings, adv_embeddings)
                        if loss_value > temp_best_loss:
                            temp_best_loss = loss_value
                            temp_best_code = temp_code
                            update_flag = True

                    adv_code = temp_best_code

                    print('Loss value increased: current loss = {}'.format(temp_best_loss))
                    
                    if update_flag:
                        for idx in range(len(sorted_id)):
                            if sorted_id[idx] >= insert_idx:
                                sorted_id[idx] += 1
                        inserted_num += 1
                    #控制插入数量
                    if inserted_num >= self.args.num_of_changes:
                        break 

        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
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

        print('success: {}, adv_code: {}'.format(is_success, adv_code))

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = [], {}, 0, {}

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words




class MHM_Attacker():
    def __init__(self, args, model_sub, model_tgt, tokenizer, model_mlm, tokenizer_mlm) -> None:
        self.classifier = model_tgt
        self.model_sub = model_sub
        self.model_mlm = model_mlm
        self.tokenizer = tokenizer
        # self.token2idx = _token2idx
        # self.idx2token = _idx2token
        self.args = args
        self.tokenizer_mlm = tokenizer_mlm

    def convert_code_to_features(self, code):
        code_tokens=self.tokenizer.tokenize(code)[:self.args.block_size-2]
        source_tokens =[self.tokenizer.cls_token]+code_tokens+[self.tokenizer.sep_token]
        source_ids =  self.tokenizer.convert_tokens_to_ids(source_tokens)
        padding_length = self.args.block_size - len(source_ids)
        source_ids+=[self.tokenizer.pad_token_id]*padding_length
        return InputFeatures(source_tokens,source_ids, 0)

    def get_feature_distance(self, orig_embeddings, adv_code):
        adv_code = ' ' + adv_code
        adv_feature = self.convert_code_to_features(adv_code).input_ids
        adv_embeddings = self.model_sub(torch.tensor(adv_feature).unsqueeze(0).to(self.args.device))[0]
        return nn.MSELoss()(orig_embeddings.to(self.args.device), adv_embeddings.to(self.args.device)).item()
        

    def convert_examples_to_features(self, code_tokens,label,url1,url2,tokenizer,args,cache):
        #source
        code_tokens=code_tokens[:args.block_size-2]
        code_tokens =[tokenizer.cls_token]+code_tokens+[tokenizer.sep_token]
        code_ids=tokenizer.convert_tokens_to_ids(code_tokens)
        padding_length = args.block_size - len(code_ids)
        code_ids+=[tokenizer.pad_token_id]*padding_length

        return InputFeatures(code_tokens,code_ids,0,label)


    def mcmc(self, example, code, substituions, _label=None, _n_candi=30,
             _max_iter=100, _prob_threshold=1):
        # code_1 = code_pair[2]
        # code_2 = code_pair[3]

        # 先得到tgt_model针对原始Example的预测信息.
        tokenizer = self.tokenizer
        self.orig_embeddings = self.model_sub(example[0].view(-1,self.args.block_size).to(self.args.device))[0]
        orig_prob = -self.get_feature_distance(self.orig_embeddings, code)
        current_prob = orig_prob

        logits, preds = self.classifier.get_results([example], self.args.eval_batch_size)
        # orig_prob = logits[0]
        orig_label = preds[0]
        # current_prob = max(orig_prob)

        true_label = example[1].item()
        adv_code = copy.deepcopy(code)
        temp_label = None


        identifiers, code_tokens = get_identifiers(code, 'python')
        prog_length = len(code_tokens)
        processed_code = " ".join(code_tokens)

        # identifiers_2, code_tokens_2 = get_identifiers(code_2, 'java')
        # processed_code_2 = " ".join(code_tokens_2)

        
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        # code_2 = " ".join(code_2.split())
        # words_2 = self.tokenizer_mlm.tokenize(code_2)

        variable_names = list(substituions.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            print('The original prediction is wrong!!!')
            return {'succ': is_success, 'adv_code': adv_code, 'tokens': None, 'raw_tokens': None}

        raw_tokens = copy.deepcopy(words)

        uid = get_identifier_posistions_from_code(words, variable_names)

        if len(uid) <= 0: # 是有可能存在找不到变量名的情况的.
            print('No identifier founded!!!')
            is_success = -4
            return {'succ': is_success, 'adv_code': adv_code, 'tokens': None, 'raw_tokens': None}

        
        variable_substitue_dict = {}
        for tgt_word in uid.keys():
            variable_substitue_dict[tgt_word] = substituions[tgt_word]
        
        old_uids = {}
        old_uid = ""
        for iteration in range(1, 1+_max_iter):
            # 这个函数需要tokens
            res = self.__replaceUID(words=words, _tokens=code, _label=true_label, _uid=uid,
                                    substitute_dict=variable_substitue_dict,
                                    _n_candi=_n_candi,
                                    _prob_threshold=_prob_threshold)
            self.__printRes(_iter=iteration, _res=res, _prefix="  >> ")
            if res['status'].lower() in ['s', 'a']:
                if iteration == 1:
                    old_uids[res["old_uid"]] = []
                    old_uids[res["old_uid"]].append(res["new_uid"])
                    old_uid = res["old_uid"]
                flag = 0
                for k in old_uids.keys():
                    if res["old_uid"] == old_uids[k][-1]:
                        flag = 1
                        old_uids[k].append(res["new_uid"])
                        old_uid = k
                        break
                if flag == 0:
                    old_uids[res["old_uid"]] = []
                    old_uids[res["old_uid"]].append(res["new_uid"])
                    old_uid = res["old_uid"]

                code = res['tokens']
                uid[res['new_uid']] = uid.pop(res['old_uid']) # 替换key，但保留value.
                variable_substitue_dict[res['new_uid']] = variable_substitue_dict.pop(res['old_uid'])
                for i in range(len(raw_tokens)):
                    if raw_tokens[i] == res['old_uid']:
                        raw_tokens[i] = res['new_uid']
                # if res['status'].lower() == 's':
                #     replace_info = {}
                #     nb_changed_pos = 0
                #     for uid_ in old_uids.keys():
                #         replace_info[uid_] = old_uids[uid_][-1]
                #         nb_changed_pos += len(uid[old_uids[uid_][-1]])
                #     return {'succ': True, 'tokens': code_1,
                #             'raw_tokens': raw_tokens, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": 1, "old_uid": old_uid, "score_info": res["old_prob"][0]-res["new_prob"][0], "nb_changed_var": len(old_uids), "nb_changed_pos":nb_changed_pos, "replace_info": replace_info, "attack_type": "MHM","orig_label": orig_label}
        replace_info = {}
        nb_changed_pos = 0
        for uid_ in old_uids.keys():
            replace_info[uid_] = old_uids[uid_][-1]
            nb_changed_pos += len(uid[old_uids[uid_][-1]])

        adv_code = code
        for tgt_word, candidate in replace_info.items():
            adv_code = get_example(adv_code, tgt_word, candidate, "python")

         #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code)
        adv_feature.label = 0    # set a pseduo label
        adv_dataset = CodeDataset([adv_feature])
        logits, preds = self.classifier.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if temp_label != true_label:
            is_success = 1
            print('Insert Attack Success!!!')
        else:
            is_success = -1

        return {'succ': is_success, 'tokens': res['tokens'], 'raw_tokens': None, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": -1, "old_uid": old_uid, "score_info": res["old_prob"]-res["new_prob"], "nb_changed_var": len(old_uids), "nb_changed_pos":nb_changed_pos, "replace_info": replace_info, "attack_type": "MHM", "orig_label": orig_label, "adv_code": adv_code}
    

    # def mcmc_random(self, example, substituions, tokenizer, code_pair, _label=None, _n_candi=30,
    #          _max_iter=100, _prob_threshold=0.95):
    #     code_1 = code_pair[2]
    #     code_2 = code_pair[3]

    #     # 先得到tgt_model针对原始Example的预测信息.

    #     logits, preds = self.classifier.get_results([example], self.args.eval_batch_size)
    #     orig_prob = logits[0]
    #     orig_label = preds[0]
    #     current_prob = max(orig_prob)

    #     true_label = example[1].item()
    #     adv_code = ''
    #     temp_label = None


    #     identifiers, code_tokens = get_identifiers(code_1, 'java')
    #     prog_length = len(code_tokens)
    #     processed_code = " ".join(code_tokens)

    #     identifiers_2, code_tokens_2 = get_identifiers(code_2, 'java')
    #     processed_code_2 = " ".join(code_tokens_2)

        
    #     words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
    #     code_2 = " ".join(code_2.split())
    #     words_2 = self.tokenizer_mlm.tokenize(code_2)

    #     variable_names = list(substituions.keys())

    #     if not orig_label == true_label:
    #         # 说明原来就是错的
    #         is_success = -4
    #         return {'succ': None, 'tokens': None, 'raw_tokens': None}

    #     raw_tokens = copy.deepcopy(words)

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
    #         res = self.__replaceUID_random(words_2=words_2, _tokens=code_1, _label=true_label, _uid=uid,
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

    #             code_1 = res['tokens']
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
    #                 return {'succ': True, 'tokens': code_1,
    #                         'raw_tokens': raw_tokens, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": 1, "old_uid": old_uid, "score_info": res["old_prob"][0]-res["new_prob"][0], "nb_changed_var": len(old_uids), "nb_changed_pos":nb_changed_pos, "replace_info":replace_info, "attack_type": "Ori_MHM","orig_label": orig_label}
    #     replace_info = {}
    #     nb_changed_pos = 0

    #     for uid_ in old_uids.keys():
    #         replace_info[uid_] = old_uids[uid_][-1]
    #         nb_changed_pos += len(uid[old_uids[uid_][-1]])
    #     return {'succ': False, 'tokens': res['tokens'], 'raw_tokens': None, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": -1, "old_uid": old_uid, "score_info": res["old_prob"][0]-res["new_prob"][0], "nb_changed_var": len(old_uids), "nb_changed_pos":nb_changed_pos, "replace_info": replace_info, "attack_type": "Ori_MHM", "orig_label": orig_label}
        
    def __replaceUID(self, words, _tokens, _label=None, _uid={}, substitute_dict={},
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
                    candi_tokens[-1] = get_example(candi_tokens[-1], selected_uid, c, "python")

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

    # def __replaceUID_random(self, words_2, _tokens=[], _label=None, _uid={}, substitute_dict={},
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
    #                 candi_tokens[-1] = get_example(candi_tokens[-1], selected_uid, c, "java")

    #         new_example = []
    #         for tmp_tokens in candi_tokens:
    #             tmp_tokens = " ".join(tmp_tokens.split())
    #             tmp_tokens = self.tokenizer_mlm.tokenize(tmp_tokens)
    #             new_feature = convert_examples_to_features(tmp_tokens, 
    #                                             words_2,
    #                                             _label, 
    #                                             None, None,
    #                                             self.tokenizer_mlm,
    #                                             self.args, None)
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
                   _res['old_pred'], _res['new_pred'],), flush=True)