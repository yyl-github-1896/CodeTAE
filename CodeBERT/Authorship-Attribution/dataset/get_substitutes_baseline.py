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

    args = parser.parse_args()

    eval_data = []

    codebert_mlm = RobertaForMaskedLM.from_pretrained(args.base_model)
    tokenizer_mlm = RobertaTokenizer.from_pretrained(args.base_model)
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

            sub_words = [tokenizer_mlm.cls_token] + sub_words[:args.block_size - 2] + [tokenizer_mlm.sep_token]
            
            input_ids_ = torch.tensor([tokenizer_mlm.convert_tokens_to_ids(sub_words)])

            word_predictions = codebert_mlm(input_ids_.to('cuda'))[0].squeeze()  # seq-len(sub) vocab
            word_pred_scores_all, word_predictions = torch.topk(word_predictions, 60, -1)  # seq-len k
            # 得到前k个结果.

            word_predictions = word_predictions[1:len(sub_words) + 1, :]
            word_pred_scores_all = word_pred_scores_all[1:len(sub_words) + 1, :]
            
            names_positions_dict = get_identifier_posistions_from_code(words, variable_names)

            variable_substitute_dict = {}

            with torch.no_grad():
                orig_embeddings = codebert_mlm.roberta(input_ids_.to('cuda'))[0]
            cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
            for tgt_word in names_positions_dict.keys():
                tgt_positions = names_positions_dict[tgt_word] # the positions of tgt_word in code
                if not is_valid_variable_name(tgt_word, lang='python'):
                    # if the extracted name is not valid
                    continue   

                ## 得到(所有位置的)substitutes
                all_substitutes = []
                for one_pos in tgt_positions:
                    ## 一个变量名会出现很多次
                    if keys[one_pos][0] >= word_predictions.size()[0]:
                        continue
                    substitutes = word_predictions[keys[one_pos][0]:keys[one_pos][1]]  # L, k
                    word_pred_scores = word_pred_scores_all[keys[one_pos][0]:keys[one_pos][1]]
                    
                    orig_word_embed = orig_embeddings[0][keys[one_pos][0]+1:keys[one_pos][1]+1]

                    similar_substitutes = []
                    similar_word_pred_scores = []
                    sims = []
                    subwords_leng, nums_candis = substitutes.size()

                    for i in range(nums_candis):

                        new_ids_ = copy.deepcopy(input_ids_)
                        new_ids_[0][keys[one_pos][0]+1:keys[one_pos][1]+1] = substitutes[:,i]
                        # 替换词得到新embeddings

                        with torch.no_grad():
                            new_embeddings = codebert_mlm.roberta(new_ids_.to('cuda'))[0]
                        new_word_embed = new_embeddings[0][keys[one_pos][0]+1:keys[one_pos][1]+1]

                        sims.append((i, sum(cos(orig_word_embed, new_word_embed))/subwords_leng))
                    
                    sims = sorted(sims, key=lambda x: x[1], reverse=True)
                    # 排序取top 30 个

                    for i in range(int(nums_candis/2)):
                        similar_substitutes.append(substitutes[:,sims[i][0]].reshape(subwords_leng, -1))
                        similar_word_pred_scores.append(word_pred_scores[:,sims[i][0]].reshape(subwords_leng, -1))

                    similar_substitutes = torch.cat(similar_substitutes, 1)
                    similar_word_pred_scores = torch.cat(similar_word_pred_scores, 1)

                    substitutes = get_substitutes(similar_substitutes, 
                                                tokenizer_mlm, 
                                                codebert_mlm, 
                                                1, 
                                                similar_word_pred_scores, 
                                                0)
                    all_substitutes += substitutes
                all_substitutes = set(all_substitutes)

                for tmp_substitute in all_substitutes:
                    if tmp_substitute.strip() in variable_names:
                        continue
                    if not is_valid_substitute(tmp_substitute.strip(), tgt_word, 'python'):
                        continue
                    try:
                        variable_substitute_dict[tgt_word].append(tmp_substitute)
                    except:
                        variable_substitute_dict[tgt_word] = [tmp_substitute]
            item["substitutes"] = variable_substitute_dict
            wf.write(json.dumps(item)+'\n')
            

if __name__ == "__main__":
    main()
