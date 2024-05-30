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
    parser.add_argument("--index", nargs='+',
                        help="Optional input sequence length after tokenization.")
    args = parser.parse_args()

    eval_data = []

    tokenizer_mlm = RobertaTokenizer.from_pretrained('../cache/Salesforce/codet5-small')

    url_to_code={}

    with open('./data.jsonl') as f:
        for line in f:
            line=line.strip()
            js=json.loads(line)
            url_to_code[js['idx']]=js['func']
    
    with open(args.eval_data_file) as f:
        for i, line in enumerate(f):
            if i < int(args.index[0]) or i >= int(args.index[1]):
                continue
            item = {}
            line=line.strip()
            url1, url2, label = line.split('\t')
            if url1 not in url_to_code or url2 not in url_to_code:
                continue
            if label=='0':
                label=0
                item["id1"] = url1
                item["id2"] = url2
                item["code1"] = url_to_code[url1]
                item["code2"] = url_to_code[url2]
                item["label"] = label
                eval_data.append(item)
            else:
                label=1
                item["id1"] = url1
                item["id2"] = url2
                item["code1"] = url_to_code[url1]
                item["code2"] = url_to_code[url2]
                item["label"] = label
                eval_data.append(item)
    print(len(eval_data))
    with open(args.store_path, "w") as wf:
        all_substitutes_set = set()

        for item in tqdm(eval_data):
            try:
                identifiers, code_tokens = get_identifiers(remove_comments_and_docstrings(item["code1"], "java"), "java")
            except:
                identifiers, code_tokens = get_identifiers(item["code1"], "java")
            processed_code = " ".join(code_tokens)
            
            words, sub_words, keys = _tokenize(processed_code, tokenizer_mlm)
            for name in identifiers:
                if ' ' in name[0].strip():
                    continue
                all_substitutes_set.add(name[0])
        print('all the variable names in the dataset have been collected!')
        print('current substitute set length: {}'.format(len(all_substitutes_set)))


        for item in tqdm(eval_data):
            try:
                identifiers, code_tokens = get_identifiers(remove_comments_and_docstrings(item["code1"], "java"), "java")
            except:
                identifiers, code_tokens = get_identifiers(item["code1"], "java")
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
                if not is_valid_variable_name(tgt_word, lang='java'):
                    # if the extracted name is not valid
                    continue
                
                for tmp_substitute in all_substitutes_set:
                    if tmp_substitute.strip() in variable_names:
                        continue
                    if not is_valid_substitute(tmp_substitute.strip(), tgt_word, 'java'):
                        continue
                    try:
                        variable_substitue_dict[tgt_word].append(tmp_substitute)
                    except:
                        variable_substitue_dict[tgt_word] = [tmp_substitute]
            item["substitutes"] = variable_substitue_dict
            wf.write(json.dumps(item)+'\n')

        print('substitute token dataset created!')



if __name__ == "__main__":
    main()
