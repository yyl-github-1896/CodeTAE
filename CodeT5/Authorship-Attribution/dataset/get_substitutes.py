import numpy as np
import os
import pickle
import json
import sys
import copy
import torch
import argparse
from tqdm import tqdm

sys.path.append('../../../')
sys.path.append('../../../python_parser')

# from attacker import 
from python_parser.run_parser import get_identifiers, remove_comments_and_docstrings
from python_parser.run_parser import python_keywords
from utils import is_valid_variable_name, _tokenize, get_identifier_posistions_from_code, get_masked_code_by_position, get_substitutes, is_valid_substitute
from transformers import (RobertaForMaskedLM, RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer)


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--eval_data_file", default=None, type=str,
                        help="An optional input evaluation data file to evaluate the perplexity on (a text file).")
    parser.add_argument("--base_model", default=None, type=str,
                        help="Base Model")
    parser.add_argument("--store_path", default=None, type=str,
                        help="results")

    parser.add_argument("--block_size", default=-1, type=int,
                        help="Optional input sequence length after tokenization.")

    args = parser.parse_args()

    eval_data = []

    try:
        codebert_mlm = RobertaForMaskedLM.from_pretrained(args.base_model)
    except:
        codebert_mlm = RobertaForMaskedLM.from_pretrained('../cache/Salesforce/codet5-small')
    try:
        tokenizer_mlm = RobertaTokenizer.from_pretrained(args.base_model)
    except:
        tokenizer_mlm = RobertaTokenizer.from_pretrained('../cache/Salesforce/codet5-small')
    codebert_mlm.to('cuda')

    file_type = args.eval_data_file.split('/')[-1].split('.')[0] # valid
    folder = '/'.join(args.eval_data_file.split('/')[:-1]) # 得到文件目录
    codes_file_path = os.path.join(folder, 'cached_{}.pkl'.format(
                                file_type))

    with open(codes_file_path, 'rb') as f:
        source_codes = pickle.load(f)

    for code in source_codes:
        item = {}
        item["code"] = code
        eval_data.append(item)


    with open(args.store_path, "w") as wf:
        all_substitues_set = set()

        for item in tqdm(eval_data):
            try:
                identifiers, code_tokens = get_identifiers(remove_comments_and_docstrings(item["code"], "python"), "python")
            except:
                identifiers, code_tokens = get_identifiers(item["code"], "python")
            processed_code = " ".join(code_tokens)
            
            words, sub_words, keys = _tokenize(processed_code, tokenizer_mlm)

            for name in identifiers:
                if ' ' in name[0].strip():
                    continue
                all_substitues_set.add(name[0])
        print('all the variable names in the dataset have been collected!')
        print('current substitute set length: {}'.format(len(all_substitues_set)))

        # all_substitues_set_temp = list(all_substitues_set)
        # for item in all_substitues_set_temp:
        #     # print('item: {}'.format(item))
        #     processed_code = " ".join(item)
        #     words, sub_words, keys = _tokenize(processed_code, tokenizer_mlm)
        #     # print('sub_words: {}'.format(sub_words))
        #     sub_words = [tokenizer_mlm.cls_token] + sub_words + [tokenizer_mlm.sep_token]
        #     input_ids_ = torch.tensor([tokenizer_mlm.convert_tokens_to_ids(sub_words)])
        #     word_predictions = codebert_mlm(input_ids_.to('cuda'))[0].squeeze()  # seq-len(sub) vocab
        #     word_pred_scores_all, word_predictions = torch.topk(word_predictions, 60, -1)  # seq-len k
        #     # 得到前k个结果.
        #     word_predictions = word_predictions[1:len(sub_words) + 1, :]
        #     word_pred_scores_all = word_pred_scores_all[1:len(sub_words) + 1, :]
        #     # print('word_predictions.shape: {}'.format(word_predictions.shape))
        #     substitutes = get_substitues(word_predictions, 
        #                                         tokenizer_mlm, 
        #                                         codebert_mlm, 
        #                                         1, 
        #                                         word_pred_scores_all, 
        #                                         0)
        #     all_substitues_set.add(substitutes[-1])

        # print('length of all_substitutes_set after update: {}'.format(len(all_substitues_set)))
            

        # '''add all possible variable names'''
        # token_list = []
        # token_list += [chr(i) for i in np.arange(97, 123)]
        # token_list += [chr(i) for i in np.arange(65, 91)]
        # token_list += [str(i) for i in range(10)]

        # token_list_first = ['_'] + [chr(i) for i in np.arange(97, 123)] + [chr(i) for i in np.arange(65, 91)]
        # token_list_all = ['', '_'] + [chr(i) for i in np.arange(97, 123)] + [chr(i) for i in np.arange(65, 91)] + [str(i) for i in range(10)]

        # all_possible_variables = []
        # for x1 in token_list_first:
        #     for x2 in token_list_all:
        #         all_possible_variables.append(x1 + x2)
        # all_possible_variables = set(all_possible_variables)
        # for item in python_keywords:
        #     if item in all_possible_variables:
        #         all_possible_variables.remove(item)
        # all_substitues_set = all_substitues_set.union(all_possible_variables) 
        # print('substitute set length after updated: {}'.format(len(all_possible_variables)))



        for item in tqdm(eval_data):
            try:
                identifiers, code_tokens = get_identifiers(remove_comments_and_docstrings(item["code"], "python"), "python")
            except:
                identifiers, code_tokens = get_identifiers(item["code"], "python")
            processed_code = " ".join(code_tokens)
            
            words, sub_words, keys = _tokenize(processed_code, tokenizer_mlm)

            variable_names = []
            for name in identifiers:
                if ' ' in name[0].strip():
                    continue
                variable_names.append(name[0])
            
            names_positions_dict = get_identifier_posistions_from_code(words, variable_names)

            variable_substitue_dict = {}

            for tgt_word in names_positions_dict.keys():
                tgt_positions = names_positions_dict[tgt_word] # the positions of tgt_word in code
                if not is_valid_variable_name(tgt_word, lang='python'):
                    # if the extracted name is not valid
                    continue   

                for tmp_substitue in all_substitues_set:
                    if tmp_substitue.strip() in variable_names:
                        continue
                    if not is_valid_substitute(tmp_substitue.strip(), tgt_word, 'python'):
                        continue
                    try:
                        variable_substitue_dict[tgt_word].append(tmp_substitue)
                    except:
                        variable_substitue_dict[tgt_word] = [tmp_substitue]
            item["substitutes"] = variable_substitue_dict
            wf.write(json.dumps(item)+'\n')
        print('substitute token dataset created!')

    return
            

if __name__ == "__main__":
    main()
