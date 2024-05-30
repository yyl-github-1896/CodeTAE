import sys
import os
import re

sys.path.append('../../../')
sys.path.append('../../../python_parser')

import csv
import copy
import json
import logging
import argparse
import warnings
import torch
import torch.nn as nn
import numpy as np
import random
from run import TextDataset, InputFeatures
from utils import select_parents, crossover, map_chromesome, mutate, is_valid_variable_name, _tokenize, get_identifier_posistions_from_code, get_masked_code_by_position, get_substitutes, is_valid_substitute, set_seed

from utils import CodeDataset
from utils import getUID, isUID, getTensor, build_vocab
from run_parser import get_identifiers, get_example
from transformers import (RobertaForMaskedLM, RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer)

def compute_fitness(chromesome, codebert_tgt, tokenizer, orig_prob, orig_label, true_label, code, names_positions_dict, args):
    # 计算fitness function.
    # words + chromesome + orig_label + current_prob
    temp_code = map_chromesome(chromesome, code, "c")

    new_feature = convert_code_to_features(temp_code, tokenizer, true_label, args)
    new_dataset = CodeDataset([new_feature])
    new_logits, preds = codebert_tgt.get_results(new_dataset, args.eval_batch_size)
    # 计算fitness function
    fitness_value = orig_prob - new_logits[0][orig_label]
    return fitness_value, preds[0]



class CrossDomainAttacker():
    def __init__(self, args, model_sub, model_tgt, tokenizer_tgt, tokenizer_mlm) -> None:
        self.args = args
        self.model_sub = model_sub
        self.model_tgt = model_tgt
        self.tokenizer = tokenizer_tgt
        self.tokenizer_mlm = tokenizer_mlm
        self.targeted = False

    def loss(self, embedding_a, embedding_b):
        '''
        compute the squared distance between embedding_a and embedding_b
        '''        
        return nn.MSELoss()(embedding_a.to(self.args.device), embedding_b.to(self.args.device)).item()

    def convert_code_to_embedding(self, code):
        input_ids = self.tokenizer(code, return_tensors="pt").input_ids.to(self.args.device)[:,:self.args.block_size]
        attention_mask = input_ids.ne(self.tokenizer.pad_token_id).to(self.args.device)
        outputs = self.model_sub(input_ids=input_ids, attention_mask=attention_mask,
                               labels=input_ids, decoder_attention_mask=attention_mask, output_hidden_states=True)['decoder_hidden_states'][-1].sum(dim=1).squeeze()
        return outputs

    def convert_code_to_features(self, code, label=0):
        code = ' '.join(code.split())
        code_tokens = self.tokenizer.tokenize(code)[:self.args.block_size-2]
        source_tokens = [self.tokenizer.cls_token] + code_tokens + [self.tokenizer.sep_token]
        source_ids = self.tokenizer.convert_tokens_to_ids(source_tokens)
        padding_length = self.args.block_size - len(source_ids)
        source_ids += [self.tokenizer.pad_token_id] * padding_length
        return InputFeatures(source_tokens, source_ids, 0, label)

    def get_importance_score(self, args, example, code, words_list: list, sub_words: list, variable_names: list, tgt_model, tokenizer, label_list, batch_size=16, max_length=512, model_type='classification'):
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

        embeddings_list = []
        for index, tokens in enumerate([words_list] + masked_token_list):
            new_code = ' '.join(tokens)
            embeddings_list.append(self.convert_code_to_embedding(new_code).detach().cpu())
        embeddings = torch.stack(embeddings_list)

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


        identifiers, code_tokens = get_identifiers(code, 'c')
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

        return np.mean(importance_score)

    def ga_attack(self, example, code, substituions, initial_replace=None):
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
            substitues for variables: replaced_words
        '''
            # 先得到tgt_model针对原始Example的预测信息.

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        current_prob = max(orig_prob)

        true_label = example[1].item()
        adv_code = ''
        temp_label = None


        identifiers, code_tokens = get_identifiers(code, 'c')
        prog_length = len(code_tokens)

        processed_code = " ".join(code_tokens)
        
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..


        variable_names = list(substituions.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None
            
        if len(variable_names) == 0:
            # 没有提取到identifier，直接退出
            is_success = -3
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        names_positions_dict = get_identifier_posistions_from_code(words, variable_names)

        nb_changed_var = 0 # 表示被修改的variable数量
        nb_changed_pos = 0
        is_success = -1

        # 我们可以先生成所有的substitues
        variable_substitue_dict = {}


        for tgt_word in names_positions_dict.keys():
            variable_substitue_dict[tgt_word] = substituions[tgt_word]


        if len(variable_substitue_dict) == 0:
            is_success = -3
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        fitness_values = []
        base_chromesome = {word: word for word in variable_substitue_dict.keys()}
        population = [base_chromesome]
        # 关于chromesome的定义: {tgt_word: candidate, tgt_word_2: candidate_2, ...}
        for tgt_word in variable_substitue_dict.keys():
            # 这里进行初始化
            if initial_replace is None:
                # 对于每个variable: 选择"影响最大"的substitues
                replace_examples = []
                substitute_list = []

                current_prob = max(orig_prob)
                most_gap = 0.0
                initial_candidate = tgt_word
                tgt_positions = names_positions_dict[tgt_word]
                
                # 原来是随机选择的，现在要找到改变最大的.
                for a_substitue in variable_substitue_dict[tgt_word]:
                    # a_substitue = a_substitue.strip()
                    
                    substitute_list.append(a_substitue)
                    # 记录下这次换的是哪个substitue
                    temp_code = get_example(code, tgt_word, a_substitue, "c") 
                    new_feature = convert_code_to_features(temp_code, self.tokenizer, example[1].item(), self.args)
                    replace_examples.append(new_feature)

                if len(replace_examples) == 0:
                    # 并没有生成新的mutants，直接跳去下一个token
                    continue
                new_dataset = CodeDataset(replace_examples)
                    # 3. 将他们转化成features
                logits, preds = self.model_tgt.get_results(new_dataset, self.args.eval_batch_size)

                _the_best_candidate = -1
                for index, temp_prob in enumerate(logits):
                    temp_label = preds[index]
                    gap = current_prob - temp_prob[temp_label]
                    # 并选择那个最大的gap.
                    if gap > most_gap:
                        most_gap = gap
                        _the_best_candidate = index
                if _the_best_candidate == -1:
                    initial_candidate = tgt_word
                else:
                    initial_candidate = substitute_list[_the_best_candidate]
            else:
                initial_candidate = initial_replace[tgt_word]

            temp_chromesome = copy.deepcopy(base_chromesome)
            temp_chromesome[tgt_word] = initial_candidate
            population.append(temp_chromesome)
            temp_fitness, temp_label = compute_fitness(temp_chromesome, self.model_tgt, self.tokenizer, max(orig_prob), orig_label, true_label , code, names_positions_dict, self.args)
            fitness_values.append(temp_fitness)

        cross_probability = 0.7

        max_iter = max(5 * len(population), 10)
        # 这里的超参数还是的调试一下.

        for i in range(max_iter):
            _temp_mutants = []
            for j in range(self.args.eval_batch_size):
                p = random.random()
                chromesome_1, index_1, chromesome_2, index_2 = select_parents(population)
                if p < cross_probability: # 进行crossover
                    if chromesome_1 == chromesome_2:
                        child_1 = mutate(chromesome_1, variable_substitue_dict)
                        continue
                    child_1, child_2 = crossover(chromesome_1, chromesome_2)
                    if child_1 == chromesome_1 or child_1 == chromesome_2:
                        child_1 = mutate(chromesome_1, variable_substitue_dict)
                else: # 进行mutates
                    child_1 = mutate(chromesome_1, variable_substitue_dict)
                _temp_mutants.append(child_1)
            
            # compute fitness in batch
            feature_list = []
            for mutant in _temp_mutants:
                _temp_code = map_chromesome(mutant, code, "c")
                _tmp_feature = convert_code_to_features(_temp_code, self.tokenizer, true_label, self.args)
                feature_list.append(_tmp_feature)
            if len(feature_list) == 0:
                continue
            new_dataset = CodeDataset(feature_list)
            mutate_logits, mutate_preds = self.model_tgt.get_results(new_dataset, self.args.eval_batch_size)
            mutate_fitness_values = []
            for index, logits in enumerate(mutate_logits):
                if mutate_preds[index] != orig_label:
                    adv_code = map_chromesome(_temp_mutants[index], code, "c")
                    for old_word in _temp_mutants[index].keys():
                        if old_word == _temp_mutants[index][old_word]:
                            nb_changed_var += 1
                            nb_changed_pos += len(names_positions_dict[old_word])

                    return code, prog_length, adv_code, true_label, orig_label, mutate_preds[index], 1, variable_names, None, nb_changed_var, nb_changed_pos, _temp_mutants[index]
                _tmp_fitness = max(orig_prob) - logits[orig_label]
                mutate_fitness_values.append(_tmp_fitness)
            
            # 现在进行替换.
            for index, fitness_value in enumerate(mutate_fitness_values):
                min_value = min(fitness_values)
                if fitness_value > min_value:
                    # 替换.
                    min_index = fitness_values.index(min_value)
                    population[min_index] = _temp_mutants[index]
                    fitness_values[min_index] = fitness_value

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, nb_changed_var, nb_changed_pos, None
        


    def greedy_attack(self, example, code, substituions):
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
            substitues for variables: replaced_words
        '''
            # 先得到tgt_model针对原始Example的预测信息.

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        current_prob = max(orig_prob)
        orig_embeddings = self.convert_code_to_embedding(code)

        current_loss = 0.0

        true_label = example[1].item()
        adv_code = code
        temp_label = None


        identifiers, code_tokens = get_identifiers(code, 'c')
        prog_length = len(code_tokens)


        processed_code = " ".join(code_tokens)
        
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        # 这里经过了小写处理..


        variable_names = list(substituions.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None
            
        if len(variable_names) == 0:
            # 没有提取到identifier，直接退出
            is_success = -3
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]
        # 如果长度超了，就截断；这里的block_size是CodeBERT能接受的输入长度
        # 计算importance_score.
        
        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score(self.args, example, 
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

        final_words = copy.deepcopy(words)
        final_code = copy.deepcopy(code)
        nb_changed_var = 0 # 表示被修改的variable数量
        nb_changed_pos = 0
        is_success = -1
        replaced_words = {}

        used_substitutes = []
        for name_and_score in sorted_list_of_names:
            tgt_word = name_and_score[0]
            tgt_positions = names_positions_dict[tgt_word]

            all_substitutes = substituions[tgt_word]

            for item in used_substitutes:
                if item in all_substitutes:
                    all_substitutes.remove(item)
            select_num = min(100, len(all_substitutes))
            all_substitutes = random.sample(all_substitutes, select_num)

            # 得到了所有位置的substitue，并使用set来去重

            most_gap = 0.0
            candidate = None
            replace_examples = []

            substitute_list = []
            new_embeddings_list = []
            # 依次记录了被加进来的substitue
            # 即，每个temp_replace对应的substitue.
            for substitute in all_substitutes:
                
                substitute_list.append(substitute)
                # 记录了替换的顺序

                # 需要将几个位置都替换成sustitue_
                temp_code = get_example(final_code, tgt_word, substitute, "c")
                new_embeddings_list.append(self.convert_code_to_embedding(temp_code).detach().cpu())
            
            best_loss = 0.0
            if self.targeted:
                for index, embed in enumerate(new_embeddings_list):
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
                    final_code = get_example(final_code, tgt_word, candidate, "c")
                    replaced_words[tgt_word] = candidate
                else:
                    replaced_words[tgt_word] = tgt_word
            else:
                for index, embed in enumerate(new_embeddings_list):
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
                    final_code = get_example(final_code, tgt_word, candidate, "c")
                    replaced_words[tgt_word] = candidate
                    used_substitutes.append(candidate)
                    if nb_changed_var >= self.args.num_of_changes:
                        break
                else:
                    replaced_words[tgt_word] = tgt_word
            
            adv_code = final_code

        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code, orig_label)
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



    def insert_attack(self, example, code, substitutes, target_example=None):


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
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + ';')
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
            if pos == 0:
                space_num = count_space(splited_code[pos])
            elif pos == len(splited_code) - 1:
                space_num = count_space(splited_code[pos])
            else:
                space_num = max(count_space(splited_code[pos]), count_space(splited_code[pos + 1]))
            splited_code.insert(pos, ' ' * space_num + variable_statement)
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + ';')
            return inserted_code_str
        
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()
        adv_code = code
        temp_label = None

        # print(example[0])
        # print(example[0].shape) #torch.Size([1020])
        orig_embeddings = self.convert_code_to_embedding(code).detach().cpu()
        

        prog_length = 0
        variable_names = list(substitutes.keys())
    
        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall(';', adv_code))
        importance_score = []

        for i in range(insert_pos_nums):
            masked_code = get_insert_masked_code(adv_code, i)
            processed_masked_code = ' ' + masked_code
            processed_masked_code = " ".join(processed_masked_code.split())
            masked_embeddings = self.convert_code_to_embedding(processed_masked_code).detach().cpu()
            importance_score.append(self.loss(orig_embeddings, masked_embeddings))

        sorted_id = sorted(range(len(importance_score)), key=lambda k: importance_score[k])
        final_code = copy.deepcopy(adv_code)
        nb_changed_pos = 0
        is_success = -1
        temp_best_loss = 0
        temp_best_code = final_code

        subs_for_insert = []
        for k, v in substitutes.items():
            subs_for_insert += v

        select_num = min(10, len(subs_for_insert))
        subs_for_insert = random.sample(subs_for_insert, select_num)

        for i, insert_idx in enumerate(sorted_id):
            if i >= self.args.num_of_changes:
                break
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, insert_idx, 'char temp_variable[100] = ' + '"' + str(sub) + '";')
                processed_adv_code = ' ' + adv_code
                adv_embeddings = self.convert_code_to_embedding(processed_adv_code).detach().cpu()
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

        adv_code = final_code
        #  query the model_tgt to see whether the attack is success
        adv_feature = self.convert_code_to_features(adv_code, orig_label)
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

        variable_names, names_to_importance_score, nb_changed_var, replaced_words = '', None, None, None
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
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.convert_code_to_embedding(code).detach().cpu()
        
        if target_example is not None:
            target_embeddings = self.convert_code_to_embedding(code).detach().cpu()
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
            processed_masked_code = ' ' + masked_code
            masked_embeddings = self.convert_code_to_embedding(processed_masked_code).detach().cpu()
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
            processed_adv_code = ' ' + adv_code
            adv_embeddings = self.convert_code_to_embedding(processed_adv_code).detach().cpu()
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

        # print('success: {}, adv_code: {}'.format(is_success, final_code))

        
        variable_names, names_to_importance_score, nb_changed_var, replaced_words = '', {}, 0, {}

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
            splited_code = code.split(';')
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
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.convert_code_to_embedding(code).detach().cpu()
        

        if target_example is not None:
            target_embeddings = self.convert_code_to_embedding(code).detach().cpu()
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
            processed_masked_code = ' ' + masked_code
            masked_embeddings = self.convert_code_to_embedding(processed_masked_code).detach().cpu()
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

        subs_for_insert = subs_for_insert[:10]  
        # print('length of subs_for_insert: {}'.format(len(subs_for_insert)))

        inserted_num = 0
        for i, inserted_id in enumerate(sorted_id):
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, inserted_id, str(sub))
                processed_adv_code = ' ' + adv_code
                adv_embeddings = self.convert_code_to_embedding(processed_adv_code).detach().cpu()
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

        # print('success: {}, adv_code: {}'.format(is_success, final_code))

        variable_names, names_to_importance_score, nb_changed_var, replaced_words = '', {}, 0, {}

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
            splited_code = code.split(';')
            splited_code.insert(pos, '<mask>')
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '; ')
            return inserted_code_str


        def get_inserted_code(code, pos, print_statement):
            splited_code = code.split(';')
            splited_code.insert(pos, 'while (0): {{ printf("{}"); }}'.format(print_statement))
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + ';')
            return inserted_code_str
        
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        adv_code = copy.deepcopy(code)
        orig_embeddings = self.convert_code_to_embedding(code).detach().cpu()
        

        if target_example is not None:
            target_embeddings = self.convert_code_to_embedding(code).detach().cpu()
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
            processed_masked_code = ' ' + masked_code
            masked_embeddings = self.convert_code_to_embedding(processed_masked_code).detach().cpu()
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

        subs_for_insert = subs_for_insert[:10]  
        # print('length of subs_for_insert: {}'.format(len(subs_for_insert)))

        inserted_num = 0
        for i, inserted_id in enumerate(sorted_id):
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, inserted_id, str(sub))
                processed_adv_code = ' ' + adv_code
                adv_embeddings = self.convert_code_to_embedding(processed_adv_code).detach().cpu()
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

        # print('success: {}, adv_code: {}'.format(is_success, final_code))

        variable_names, names_to_importance_score, nb_changed_var, replaced_words = '', {}, 0, {}

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words