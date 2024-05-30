import sys

sys.path.append('../../../')
sys.path.append('../../../python_parser')

import re
import math
import copy
import torch
torch.set_printoptions(profile="full")
import torch.nn as nn
import random
import numpy as np
from run import InputFeatures, convert_examples_to_features
from utils import select_parents, crossover, map_chromesome, mutate, is_valid_variable_name, _tokenize, get_identifier_posistions_from_code, get_masked_code_by_position, set_seed

from utils import CodeDataset
from utils import getUID, isUID, getTensor, build_vocab
from run_parser import get_identifiers, get_example
from transformers import (RobertaForMaskedLM, RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer)



class CrossDomainAttacker():
    def __init__(self, args, model_sub, model_tgt, tokenizer, model_mlm, tokenizer_mlm, use_bpe, threshold_pred_score, targeted=False) -> None:
        self.args = args
        self.model_sub = model_sub                          # substitute model (input: token_ids, output: embeddings)
        self.model_tgt = model_tgt                          # target model (input: tokens_ids, output: classify_logits)
        self.tokenizer = tokenizer                      # tokenizer of the substitute & target model
        self.model_mlm = model_mlm
        self.tokenizer_mlm = tokenizer_mlm
        self.use_bpe = use_bpe
        self.threshold_pred_score = threshold_pred_score
        self.targeted = targeted

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

    def compute_fitness(self, chromesome, words_2, codebert_tgt, tokenizer_tgt, orig_prob, orig_label, true_label ,code, names_positions_dict, args, orig_example=None, target_example=None):
        # 计算fitness function.
        # words + chromesome + orig_label + current_prob
        temp_code = map_chromesome(chromesome, code, "java")
        temp_code = ' '.join(temp_code.split())
        temp_code = self.tokenizer.tokenize(temp_code)
        new_embeddings = self.convert_code_to_embedding(temp_code)
        orig_embeddings = self.convert_code_to_embedding(temp_code)
        fitness_value = self.loss(orig_embeddings, new_embeddings)
        return fitness_value


    def get_importance_score(self, args, example, code, code_2, words_list: list, sub_words: list, variable_names: list, tgt_model, label_list, batch_size=16, max_length=512, model_type='classification', target_example=None):
        '''Compute the importance score of each variable'''
        # label: example[1] tensor(1)
        # 1. 过滤掉所有的keywords.
        positions = get_identifier_posistions_from_code(words_list, variable_names)
        # 需要注意大小写.
        if len(positions) == 0:
            ## 没有提取出可以mutate的position
            print('Error! (in get_importance_score) len(positions)==0')
            return None, None, None

        new_examples = []

        # 2. 得到Masked_tokens
        masked_token_list, replace_token_positions = get_masked_code_by_position(words_list, positions)
        # replace_token_positions 表示着，哪一个位置的token被替换了.
        
        code2_tokens, _, _ = _tokenize(code_2, self.tokenizer)

        embeddings_list = []
        for index, code1_tokens in enumerate([words_list] + masked_token_list):
            code1_tokens = ' '.join(code1_tokens)
            embeddings_list.append(self.convert_code_to_embedding(code1_tokens).detach().cpu())  
        embeddings = torch.stack(embeddings_list)

        orig_embeddings = embeddings[0]
        importance_score = []
        for embed in embeddings[1:]:
            if self.targeted:
                importance_score.append(self.loss(orig_embeddings, target_embeddings) - self.loss(embed, target_embeddings))
            else:
                importance_score.append(self.loss(embed, orig_embeddings))

        return importance_score, replace_token_positions, positions

    def get_importance_score_explain(self, args, example, code, code_2, words_list: list, sub_words: list, variable_names: list, tgt_model, tokenizer, label_list, batch_size=16, max_length=512, model_type='classification'):
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
        
        code2_tokens, _, _ = _tokenize(code_2, tokenizer)

        for index, code1_tokens in enumerate([words_list] + masked_token_list):
            new_feature = convert_examples_to_features(code1_tokens,code2_tokens,example[1].item(), None, None,tokenizer,args)
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

    def variable_influence_value(self, example, substitutes, code):
        code_1 = code[2]
        code_2 = code[3]
        adv_code = copy.deepcopy(code_1)
        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        # print(logits)
        # print(preds)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()

        #剔除替换词中包含原变量名
        for k, _ in substitutes.items():
            if k in substitutes[k]:
                substitutes[k].remove(k)
        identifiers, code_tokens = get_identifiers(adv_code, 'java') # 只得到code_1中的identifier
        processed_code = " ".join(code_tokens)
        prog_length = len(code_tokens)

        identifiers_2, code_tokens_2 = get_identifiers(code_2, 'java')
        processed_code_2 = " ".join(code_tokens_2)
        
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        code_2 = " ".join(code_2.split())
        words_2 = self.tokenizer_mlm.tokenize(code_2)

        variable_names = list(substitutes.keys())
        if not orig_label == true_label:
            # 说明原来就是错的
            return None
        
        if len(variable_names) == 0:
            # 没有提取到identifier，直接退出
            return None

        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]

        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score_explain(self.args, example, 
                                                processed_code, processed_code_2,
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

    def greedy_attack(self, example, substitutes, code, target_example=None):
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

        code_1 = code[2]
        code_2 = code[3]

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()
        adv_code = copy.deepcopy(code_1)
        temp_label = None

        #剔除替换词中包含原变量名
        for k, _ in substitutes.items():
            if k in substitutes[k]:
                substitutes[k].remove(k)
        orig_embeddings = self.convert_code_to_embedding(code_1).detach().cpu()
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0
        
        # random initialization the adv_code
        replaced_words = {}
        identifiers, code_tokens = get_identifiers(adv_code, 'java') 
        used_substitutes = []
        for tgt_word in identifiers:
            tgt_word = tgt_word[0]
            all_substitutes = substitutes[tgt_word]
            for item in used_substitutes:
                if item in all_substitutes:
                    all_substitutes.remove(item)
            substitute = random.choice(all_substitutes)
            replaced_words[tgt_word] = substitute
            substitutes[substitute] = all_substitutes
            used_substitutes.append(substitute)
            adv_code = get_example(adv_code, tgt_word, substitute, 'java')

        # When do attack, we only attack the first code snippet
        identifiers, code_tokens = get_identifiers(adv_code, 'java') # 只得到code_1中的identifier
        processed_code = " ".join(code_tokens)
        prog_length = len(code_tokens)

        identifiers_2, code_tokens_2 = get_identifiers(code_2, 'java')
        processed_code_2 = " ".join(code_tokens_2)

        
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        code_2 = " ".join(code_2.split())
        words_2 = self.tokenizer_mlm.tokenize(code_2)


        variable_names = list(substitutes.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None
            
        if len(variable_names) == 0:
            # 没有提取到identifier，直接退出
            is_success = -3
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None

        sub_words = [self.tokenizer.cls_token] + sub_words[:self.args.block_size - 2] + [self.tokenizer.sep_token]

        importance_score, replace_token_positions, names_positions_dict = self.get_importance_score(self.args, example, 
                                                processed_code, processed_code_2,
                                                words,
                                                sub_words,
                                                variable_names,
                                                self.model_tgt, 
                                                [0,1], 
                                                batch_size=self.args.eval_batch_size, 
                                                max_length=self.args.block_size, 
                                                model_type='classification')

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
        
        used_substitutes = []
        for idx, name_and_score in enumerate(sorted_list_of_names):
            tgt_word = name_and_score[0]
            
            all_substitutes = substitutes[tgt_word]
            for item in used_substitutes:
                if item in all_substitutes:
                    all_substitutes.remove(item)
            select_num = min(100, len(all_substitutes))
            all_substitutes = random.sample(all_substitutes, select_num)

            best_loss = math.inf if self.targeted else 0.0
            candidate = None
            replace_examples = []

            replace_embeddings_list = []
            # 依次记录了被加进来的substitue
            # 即，每个temp_replace对应的substitue.
            substitute_list = []

            for substitute in all_substitutes:
                substitute_list.append(substitute)
                # 记录了替换的顺序
                temp_replace = get_example(final_code, tgt_word, substitute, "java")
                temp_replace = " ".join(temp_replace.split())
                replace_embeddings_list.append(self.convert_code_to_embedding(temp_replace).detach().cpu())
                
            if len(replace_embeddings_list) == 0:
                # 并没有生成新的mutants，直接跳去下一个token
                continue

            if self.targeted:
                for index, embed in enumerate(replace_embeddings_list):
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
                    final_code = get_example(final_code, tgt_word, candidate, "java")
                    replaced_words[tgt_word] = candidate
                else:
                    replaced_words[tgt_word] = tgt_word
            else:
                for index, embed in enumerate(replace_embeddings_list):
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
                    final_code = get_example(final_code, tgt_word, candidate, "java")
                    replaced_words[tgt_word] = candidate
                    used_substitutes.append(candidate)
                    if nb_changed_var >= self.args.num_of_changes:
                        break
                else:
                    replaced_words[tgt_word] = tgt_word
            
            adv_code = final_code

        #  query the model_tgt to see whether the attack is success
        temp_adv_code = adv_code
        temp_adv_code = ' '.join(temp_adv_code.split())
        temp_adv_code = self.tokenizer.tokenize(temp_adv_code)
        adv_feature = convert_examples_to_features(temp_adv_code, 
                                                words_2,
                                                true_label,
                                                None, None,
                                                self.tokenizer,
                                                self.args)
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

        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



    def insert_attack(self, example, substitutes, code, adv=None, target_example=None):

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
        
        code_1 = code[2]
        code_2 = code[3]
        
        if adv is not None:
            code_1 = adv

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()
        adv_code = copy.deepcopy(code_1)
        temp_label = None

        # print(example[0])
        # print(example[0].shape) #torch.Size([1020])
        orig_embeddings = self.convert_code_to_embedding(code_1).detach().cpu()
        

        code_2 = " ".join(code_2.split())
        words_2 = self.tokenizer_mlm.tokenize(code_2)
        prog_length = 0
        variable_names = list(substitutes.keys())
    
        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall('\n', adv_code))
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

        select_num = min(100, len(subs_for_insert))
        subs_for_insert = random.sample(subs_for_insert, select_num)

        for i, insert_idx in enumerate(sorted_id):
            if i >= self.args.num_of_changes:
                break
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, insert_idx, 'String temp_variable = ' + "'" + str(sub) + "';")
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

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        temp_adv_code = adv_code
        temp_adv_code = ' '.join(temp_adv_code.split())
        temp_adv_code = self.tokenizer.tokenize(temp_adv_code)
        adv_feature = convert_examples_to_features(temp_adv_code, 
                                                words_2,
                                                true_label,
                                                None, None,
                                                self.tokenizer,
                                                self.args)
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

        variable_names, names_to_importance_score, nb_changed_var, replaced_words = None, None, None, None
        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words



    def empty_print_attack(self, example, substitutes, code, adv=None, target_example=None):

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

        def get_inserted_code(code, pos, variable_statement='System.out.print("");'):
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

        code_1 = code[2]
        code_2 = code[3]
        
        if adv is not None:
            code_1 = adv

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()
        adv_code = copy.deepcopy(code_1)
        temp_label = None

        orig_embeddings = self.convert_code_to_embedding(code_1).detach().cpu()
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0

        code_2 = " ".join(code_2.split())
        words_2 = self.tokenizer_mlm.tokenize(code_2)
        prog_length = 0
        variable_names = list(substitutes.keys())
    
        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall('\n', adv_code))
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


        for i, inserted_id in enumerate(sorted_id):
            if i >= self.args.num_of_changes:
                break
            update_flag = False
            adv_code = get_inserted_code(final_code, inserted_id)
            processed_adv_code = ' ' + adv_code
            processed_adv_code = " ".join(processed_adv_code.split())
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

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        temp_adv_code = adv_code
        temp_adv_code = ' '.join(temp_adv_code.split())
        temp_adv_code = self.tokenizer.tokenize(temp_adv_code)
        adv_feature = convert_examples_to_features(temp_adv_code, 
                                                words_2,
                                                true_label,
                                                None, None,
                                                self.tokenizer,
                                                self.args)
        adv_dataset = CodeDataset([adv_feature])
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('Print Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('Print Attack Success!!!')
            else:
                is_success = -1

        variable_names, names_to_importance_score, nb_changed_var, replaced_words = None, None, None, None
        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words




    def nonreachable_if_attack(self, example, substitutes, code, adv=None, target_example=None):
        
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
            splited_code.insert(pos, ' ' * space_num + 'if False:\n' + ' ' * (space_num + 4) + 'System.out.print("{}");'.format(print_statement))
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str

        code_1 = code[2]
        code_2 = code[3]
        
        if adv is not None:
            code_1 = adv

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()
        adv_code = copy.deepcopy(code_1)
        temp_label = None

        # print(example[0])
        # print(example[0].shape) #torch.Size([1020])
        orig_embeddings = self.convert_code_to_embedding(code_1).detach().cpu()
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0

        code_2 = " ".join(code_2.split())
        words_2 = self.tokenizer_mlm.tokenize(code_2)
        prog_length = 0
        variable_names = list(substitutes.keys())
    
        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall('\n', adv_code))
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

        for k, v in substitutes.items():
            subs_for_insert = v
            break

        select_num = min(100, len(subs_for_insert))
        subs_for_insert = random.sample(subs_for_insert, select_num)

        for i, insert_idx in enumerate(sorted_id):
            if i >= self.args.num_of_changes:
                break
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, insert_idx, str(sub))
                processed_adv_code = ' ' + adv_code
                processed_adv_code = " ".join(processed_adv_code.split())
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

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        temp_adv_code = adv_code
        temp_adv_code = ' '.join(temp_adv_code.split())
        temp_adv_code = self.tokenizer.tokenize(temp_adv_code)
        adv_feature = convert_examples_to_features(temp_adv_code, 
                                                words_2,
                                                true_label,
                                                None, None,
                                                self.tokenizer,
                                                self.args)
        adv_dataset = CodeDataset([adv_feature])
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('If Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('If Attack Success!!!')
            else:
                is_success = -1

        variable_names, names_to_importance_score, nb_changed_var, replaced_words = None, None, None, None
        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words


    def nonreachable_while_attack(self, example, substitutes, code, adv=None, target_example=None):

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
            splited_code.insert(pos, ' ' * space_num + 'while False:\n' + ' ' * (space_num + 4) + 'System.out.print("{}");'.format(print_statement))
            inserted_code_str = ''
            for line in splited_code:
                inserted_code_str += (line + '\n')
            return inserted_code_str


        code_1 = code[2]
        code_2 = code[3]
        
        if adv is not None:
            code_1 = adv

        logits, preds = self.model_tgt.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        true_label = example[1].item()
        adv_code = copy.deepcopy(code_1)
        temp_label = None

        # print(example[0])
        # print(example[0].shape) #torch.Size([1020])
        orig_embeddings = self.convert_code_to_embedding(code_1).detach().cpu()
        
        if self.targeted:
            current_loss = self.loss(orig_embeddings, target_embeddings)
        else:
            current_loss = 0.0

        code_2 = " ".join(code_2.split())
        words_2 = self.tokenizer_mlm.tokenize(code_2)
        prog_length = 0
        variable_names = list(substitutes.keys())
    
        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, None, None, None, None


        insert_pos_nums = len(re.findall('\n', adv_code))
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

        for k, v in substitutes.items():
            subs_for_insert = v
            break

        select_num = min(100, len(subs_for_insert))
        subs_for_insert = random.sample(subs_for_insert, select_num)

        for i, insert_idx in enumerate(sorted_id):
            if i >= self.args.num_of_changes:
                break
            update_flag = False
            for sub in subs_for_insert:
                adv_code = get_inserted_code(final_code, insert_idx, str(sub))
                processed_adv_code = ' ' + adv_code
                processed_adv_code = " ".join(processed_adv_code.split())
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

        adv_code = temp_best_code
        #  query the model_tgt to see whether the attack is success
        temp_adv_code = adv_code
        temp_adv_code = ' '.join(temp_adv_code.split())
        temp_adv_code = self.tokenizer.tokenize(temp_adv_code)
        adv_feature = convert_examples_to_features(temp_adv_code, 
                                                words_2,
                                                true_label,
                                                None, None,
                                                self.tokenizer,
                                                self.args)
        adv_dataset = CodeDataset([adv_feature])
        logits, preds = self.model_tgt.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]
        if self.targeted:
            target_label = target_example[1]
            if temp_label == target_label:
                is_success = 1
                print('While Attack Success!!!')
            else:
                is_success = -1
        else:
            if temp_label != true_label:
                is_success = 1
                print('While Attack Success!!!')
            else:
                is_success = -1

        variable_names, names_to_importance_score, nb_changed_var, replaced_words = None, None, None, None
        return code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words




class MHM_Attacker():
    def __init__(self, args, model_sub, model_tgt, model_mlm, tokenizer, tokenizer_mlm) -> None:
        self.classifier = model_tgt
        self.model_sub = model_sub
        self.model_mlm = model_mlm
        # self.token2idx = _token2idx
        # self.idx2token = _idx2token
        self.args = args
        self.tokenizer = tokenizer
        self.tokenizer_mlm = tokenizer_mlm
    
    def loss(self, embedding_a, embedding_b):
        '''
        compute the squared distance between embedding_a and embedding_b
        '''        
        return nn.MSELoss()(embedding_a.to(self.args.device), embedding_b.to(self.args.device)).item()


    def mcmc(self, example, substituions, tokenizer, code_pair, _label=None, _n_candi=30,
             _max_iter=100, _prob_threshold=0.95):
        code_1 = code_pair[2]
        code_2 = code_pair[3]
    
        # 先得到tgt_model针对原始Example的预测信息.
        self.orig_embeddings = self.model_sub(example[0].to(self.args.device))

        logits, preds = self.classifier.get_results([example], self.args.eval_batch_size)
        orig_prob = logits[0]
        orig_label = preds[0]
        # current_prob = max(orig_prob)

        true_label = example[1].item()
        adv_code = copy.deepcopy(code_1)
        temp_label = None


        identifiers, code_tokens = get_identifiers(code_1, 'java')
        prog_length = len(code_tokens)
        processed_code = " ".join(code_tokens)

        identifiers_2, code_tokens_2 = get_identifiers(code_2, 'java')
        processed_code_2 = " ".join(code_tokens_2)

        
        words, sub_words, keys = _tokenize(processed_code, self.tokenizer_mlm)
        code_2 = " ".join(code_2.split())
        words_2 = self.tokenizer_mlm.tokenize(code_2)

        variable_names = list(substituions.keys())

        if not orig_label == true_label:
            # 说明原来就是错的
            is_success = -4
            return {'succ': is_success, 'adv_code': adv_code, 'tokens': None, 'raw_tokens': None}

        raw_tokens = copy.deepcopy(words)

        uid = get_identifier_posistions_from_code(words, variable_names)

        if len(uid) <= 0: # 是有可能存在找不到变量名的情况的.
            return {'succ': None, 'tokens': None, 'raw_tokens': None}

        
        variable_substitue_dict = {}
        for tgt_word in uid.keys():
            variable_substitue_dict[tgt_word] = substituions[tgt_word]
        
        old_uids = {}
        old_uid = ""
        for iteration in range(1, 1+_max_iter):
            # 这个函数需要tokens
            res = self.__replaceUID(words_2=words_2, _tokens=code_1, _label=true_label, _uid=uid,
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

                code_1 = res['tokens']
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

        adv_code = code_1
        for tgt_word, candidate in replace_info.items():
            adv_code = get_example(adv_code, tgt_word, candidate, "java")

        #  query the model_tgt to see whether the attack is success
        temp_adv_code = adv_code
        temp_adv_code = ' '.join(temp_adv_code.split())
        temp_adv_code = self.tokenizer.tokenize(temp_adv_code)
        adv_feature = convert_examples_to_features(temp_adv_code, 
                                                words_2,
                                                _label,
                                                None, None,
                                                self.tokenizer,
                                                self.args, None)
        adv_dataset = CodeDataset([adv_feature])
        logits, preds = self.classifier.get_results(adv_dataset, self.args.eval_batch_size)
        logit, temp_label = logits[0], preds[0]

        if temp_label != true_label:
            is_success = 1
            print('MHM Attack Success!!!')
        else:
            is_success = -1

        return {'succ': is_success, 'adv_code': adv_code, 'tokens': res['tokens'], 'raw_tokens': None, "prog_length": prog_length, "new_pred": res["new_pred"], "is_success": -1, "old_uid": old_uid, "score_info": res["old_prob"]-res["new_prob"], "nb_changed_var": len(old_uids), "nb_changed_pos":nb_changed_pos, "replace_info": replace_info, "attack_type": "MHM", "orig_label": orig_label}
    
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
        
    def __replaceUID(self, words_2, _tokens, _label=None, _uid={}, substitute_dict={},
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
                    candi_tokens[-1] = get_example(candi_tokens[-1], selected_uid, c, "java")

            feature_distances = []
            for tmp_tokens in candi_tokens:
                tmp_tokens = " ".join(tmp_tokens.split())
                tmp_tokens = self.tokenizer_mlm.tokenize(tmp_tokens)
                new_feature = convert_examples_to_features(tmp_tokens, 
                                                words_2,
                                                _label, 
                                                None, None,
                                                self.tokenizer_mlm,
                                                self.args, None).input_ids
                adv_embeddings = self.model_sub(torch.tensor(new_feature).to(self.args.device)).detach().cpu()
                feature_distances.append(self.loss(self.orig_embeddings, adv_embeddings))


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
                   _res['old_pred'], _res['new_pred']), flush=True)