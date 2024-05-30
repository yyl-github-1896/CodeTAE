import numpy as np
import os
import pickle
import json
import sys
import copy
import torch
import argparse
from tqdm import tqdm
import random

sys.path.append('../../../')
sys.path.append('../../../python_parser')

# from attacker import 
from python_parser.run_parser import get_identifiers, remove_comments_and_docstrings
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

    try:
        codebert_mlm = RobertaForMaskedLM.from_pretrained(args.base_model)
    except:
        codebert_mlm = RobertaForMaskedLM.from_pretrained('../cache/microsoft/codebert-base-mlm/')
    try:
        tokenizer_mlm = RobertaTokenizer.from_pretrained(args.base_model)
    except:
        tokenizer_mlm = RobertaTokenizer.from_pretrained('../cache/microsoft/codebert-base-mlm/')
    codebert_mlm.to('cuda')

    # file_type = args.eval_data_file.split('/')[-1].split('.')[0] # valid
    # folder = '/'.join(args.eval_data_file.split('/')[:-1]) # 得到文件目录
    # codes_file_path = os.path.join(folder, 'cached_{}.pkl'.format(
    #                             file_type))

    eval_data = []
    with open(args.eval_data_file) as f:
        for i, line in enumerate(f):
            if i < 0 or i >= 4000:
                continue
            item = json.loads(line.strip())
            eval_data.append(item)

    # print('keys: {}'.format(eval_data[0].keys()))


    with open(args.store_path, "w") as wf:
        all_substitues_set = set()

        for item in tqdm(eval_data):
            # try:
            identifiers, code_tokens = get_identifiers(remove_comments_and_docstrings(item["func"], "c"), "c")
            # except:
            #     identifiers, code_tokens = get_identifiers(item["func"], "c")
            processed_code = " ".join(code_tokens)
            
            words, sub_words, keys = _tokenize(processed_code, tokenizer_mlm)

            for name in identifiers:
                if ' ' in name[0].strip():
                    continue
                all_substitues_set.add(name[0])
        print('all the variable names in the dataset have been collected!')
        print('current substitute set length: {}'.format(len(all_substitues_set)))


        for item in tqdm(eval_data):
            identifiers, code_tokens = get_identifiers(remove_comments_and_docstrings(item["func"], "c"), "c")
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
                if not is_valid_variable_name(tgt_word, lang='c'):
                    # if the extracted name is not valid
                    continue   

                for tmp_substitue in all_substitues_set:
                    if tmp_substitue.strip() in variable_names:
                        continue
                    if not is_valid_substitute(tmp_substitue.strip(), tgt_word, 'c'):
                        continue
                    try:
                        variable_substitue_dict[tgt_word].append(tmp_substitue)
                    except:
                        variable_substitue_dict[tgt_word] = [tmp_substitue]
                
                variable_substitue_dict[tgt_word] = random.sample(variable_substitue_dict[tgt_word], 6)
            
            item["substitutes"] = variable_substitue_dict
            wf.write(json.dumps(item)+'\n')
        print('substitute token dataset created!')

    return
            

if __name__ == "__main__":
    main()
