
'''For attacking CodeBERT models'''
import json
import sys
import os

sys.path.append('../../../')
sys.path.append('../../../python_parser')
retval = os.getcwd()

import csv
import logging
import argparse
import warnings
import pickle
import copy
import torch
import time
import numpy as np

from model import CodeT5
from utils import set_seed
from utils import Recorder
from run import TextDataset
from attacker_crossdomain import CrossDomainAttacker
from transformers import RobertaForMaskedLM
from transformers import (T5Config, T5ForConditionalGeneration, RobertaTokenizer, RobertaModel)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.simplefilter(action='ignore', category=FutureWarning) # Only report warning

MODEL_CLASSES = {
    't5': (T5Config, T5ForConditionalGeneration, RobertaTokenizer),
}

logger = logging.getLogger(__name__)

def get_code_pairs(file_path):
    postfix=file_path.split('/')[-1].split('.txt')[0]
    folder = '/'.join(file_path.split('/')[:-1]) # 得到文件目录
    code_pairs_file_path = os.path.join(folder, 'cached_{}.pkl'.format(
                                    postfix))
    with open(code_pairs_file_path, 'rb') as f:
        code_pairs = pickle.load(f)
    return code_pairs


def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--train_data_file", default=None, type=str, required=True,
                        help="The input training data file (a text file).")
    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the model predictions and checkpoints will be written.")

    ## Other parameters
    parser.add_argument("--eval_data_file", default=None, type=str,
                        help="An optional input evaluation data file to evaluate the perplexity on (a text file).")
    parser.add_argument("--test_data_file", default=None, type=str,
                        help="An optional input evaluation data file to evaluate the perplexity on (a text file).")
    parser.add_argument("--base_model", default=None, type=str,
                        help="Base Model")
    parser.add_argument("--model_type", default="bert", type=str,
                        help="The model architecture to be fine-tuned.")
    parser.add_argument("--model_name_or_path", default=None, type=str,
                        help="The model checkpoint for weights initialization.")
    parser.add_argument("--csv_store_path", default=None, type=str,
                        help="Base Model")
    parser.add_argument("--use_ga", action='store_true',
                        help="Whether to GA-Attack.")
    parser.add_argument("--mlm", action='store_true',
                        help="Train with masked-language modeling loss instead of language modeling.")
    parser.add_argument("--mlm_probability", type=float, default=0.15,
                        help="Ratio of tokens to mask for masked language modeling loss")

    # Hyper-parameters
    parser.add_argument("--num_of_changes", required=True, type=int,
                        help="number of inserted obfuscations.")

    parser.add_argument("--config_name", default="", type=str,
                        help="Optional pretrained config name or path if not the same as model_name_or_path")
    parser.add_argument("--tokenizer_name", default="", type=str,
                        help="Optional pretrained tokenizer name or path if not the same as model_name_or_path")
    parser.add_argument("--cache_dir", default="", type=str,
                        help="Optional directory to store the pre-trained models downloaded from s3 (instread of the default one)")
    parser.add_argument("--block_size", default=-1, type=int,
                        help="Optional input sequence length after tokenization."
                             "The training dataset will be truncated in block of this size for training."
                             "Default to the model max input length for single sentence inputs (take into account special tokens).")
    parser.add_argument("--do_train", action='store_true',
                        help="Whether to run training.")
    parser.add_argument("--do_eval", action='store_true',
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--do_test", action='store_true',
                        help="Whether to run eval on the dev set.")    
    parser.add_argument("--evaluate_during_training", action='store_true',
                        help="Run evaluation during training at each logging step.")
    parser.add_argument("--eval_batch_size", default=4, type=int,
                        help="Batch size per GPU/CPU for evaluation.")
    parser.add_argument('--seed', type=int, default=42,
                        help="random seed for initialization")

    

    args = parser.parse_args()

    device = torch.device("cuda")
    args.device = device

    # Set seed
    set_seed(args.seed)

    args.start_epoch = 0
    args.start_step = 0
    checkpoint_last = os.path.join(args.output_dir, 'checkpoint-last')
    if os.path.exists(checkpoint_last) and os.listdir(checkpoint_last):
        args.model_name_or_path = os.path.join(checkpoint_last, 'pytorch_model.bin')
        args.config_name = os.path.join(checkpoint_last, 'config.json')
        idx_file = os.path.join(checkpoint_last, 'idx_file.txt')
        with open(idx_file, encoding='utf-8') as idxf:
            args.start_epoch = int(idxf.readlines()[0].strip()) + 1

        step_file = os.path.join(checkpoint_last, 'step_file.txt')
        if os.path.exists(step_file):
            with open(step_file, encoding='utf-8') as stepf:
                args.start_step = int(stepf.readlines()[0].strip())

        logger.info("reload model from {}, resume from {} epoch".format(checkpoint_last, args.start_epoch))

    config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]
    config = config_class.from_pretrained('../cache/Salesforce/codet5-base/')
    config.num_labels=2
    tokenizer = RobertaTokenizer.from_pretrained('../cache/Salesforce/codet5-base/')

    if args.block_size <= 0:
        args.block_size = tokenizer.max_len_single_sentence  # Our input block size will be the max possible for the model
    args.block_size = min(args.block_size, tokenizer.max_len_single_sentence)
    if args.model_name_or_path:
        model_tgt = model_class.from_pretrained('../cache/Salesforce/codet5-base/')    
    else:
        model_tgt = model_class(config)

    model_tgt = CodeT5(model_tgt,config,tokenizer,args).to(args.device)

    checkpoint_prefix = 'checkpoint-best-f1/model.bin'
    output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
    model_tgt.load_state_dict(torch.load(output_dir))
    model_tgt.to(args.device)


    try:
        model_sub = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-base").to(args.device)
    except:
        model_sub = T5ForConditionalGeneration.from_pretrained('../cache/Salesforce/codet5-base/').to(args.device)


    ## Load CodeBERT (MLM) model
    codebert_mlm = model_sub
    tokenizer_mlm = tokenizer
    codebert_mlm.to('cuda') 
    
    ## Load tensor features
    eval_dataset = TextDataset(tokenizer, args, args.eval_data_file)
    ## Load code pairs
    source_codes = get_code_pairs(args.eval_data_file)

    postfix = args.eval_data_file.split('/')[-1].split('.txt')[0].split("_")
    folder = '/'.join(args.eval_data_file.split('/')[:-1]) # 得到文件目录

    '''***********************************switch substitutes here*********************************'''
    subs_path = os.path.join(folder, 'test_subs_{}_{}.jsonl'.format(
                                    postfix[-2], postfix[-1]))
    substitutes = []
    with open(subs_path) as f:
        for line in f:
            js = json.loads(line.strip())
            substitutes.append(js["substitutes"])
    assert len(source_codes) == len(eval_dataset) == len(substitutes)


    '''***********************************add another subs dataset here*********************************'''
    subs_path = os.path.join(folder, 'test_subs_gan_{}_{}.jsonl'.format(
                                    postfix[-2], postfix[-1]))
    substitutes_2 = []
    with open(subs_path) as f:
        for line in f:
            js = json.loads(line.strip())
            substitutes_2.append(js["substitutes"])
    assert len(source_codes) == len(eval_dataset) == len(substitutes)


    success_attack = 0
    total_cnt = 0

    recoder = Recorder(args.csv_store_path)
    attacker = CrossDomainAttacker(args, model_sub, model_tgt, tokenizer, codebert_mlm, tokenizer_mlm, use_bpe=1, threshold_pred_score=0)
    start_time = time.time()
    query_times = 0
    adv_example = []
    for index, example in enumerate(eval_dataset):
        example_start_time = time.time()
        code_pair = source_codes[index]
        subs = substitutes[index]
        subs_2 = substitutes_2[index]
        code, prog_length, adv_code_after_greedy, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example,  subs, code_pair)
        attack_type = "Greedy"
        if is_success == -1:
            code, prog_length, adv_code_after_greedy, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example,  subs_2, code_pair)
        
        if is_success == -1:
            code_pair[0] = adv_code_after_greedy
            attacker.args.num_of_changes = 6
            code, prog_length, adv_code_after_insert, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example,  subs, code_pair)
            if is_success == -1:
                code, prog_length, adv_code_after_insert, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example,  subs_2, code_pair)

        if is_success == -1:
            code_pair[0] = adv_code_after_insert
            attacker.args.num_of_changes = 15
            code, prog_length, adv_code_after_if, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example,  subs, code_pair)
            if is_success == -1:
                code, prog_length, adv_code_after_if, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example,  subs, code_pair)

        if is_success == -1:
            code_pair[0] = adv_code_after_insert
            attacker.args.num_of_changes = 15
            code, prog_length, adv_code_after_while, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example,  subs, code_pair)
            if is_success == -1:
                code, prog_length, adv_code_after_while, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example,  subs, code_pair)

        adv_code = adv_code_after_while

        example_end_time = (time.time()-example_start_time)/60
        
        print("Example time cost: ", round(example_end_time, 2), "min")
        print("ALL examples time cost: ", round((time.time()-start_time)/60, 2), "min")

        score_info = ''
        if names_to_importance_score is not None:
            for key in names_to_importance_score.keys():
                score_info += key + ':' + str(names_to_importance_score[key]) + ','

        replace_info = ''
        variable_names = []
        if replaced_words is not None:
            for key in replaced_words.keys():
                replace_info += key + ':' + replaced_words[key] + ','

        recoder.write(index, code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, score_info, nb_changed_var, nb_changed_pos, replace_info, attack_type, 0, example_end_time)
        
        query_times = 0

        #--------------------------------------------------------------------------------------------
        # print('type: ', type(adv_code)) #type:  <class 'str'>
        
        lines_after_removal = []
        for a_line in adv_code.splitlines(True):
            if  a_line.strip().startswith("import") or a_line.strip().startswith("#") or a_line.strip().startswith("from"):
                continue
            lines_after_removal.append(a_line)
        
        content = "".join(lines_after_removal)
        new_content = content + ' <CODESPLIT> ' + str(example[1].item()) + '\n'
        adv_example.append(new_content)
        print(new_content)
        #--------------------------------------------------------------------------------------------


        if is_success >= -1 :
            # 如果原来正确
            total_cnt += 1
        if is_success == 1:
            success_attack += 1
        
        if total_cnt == 0:
            continue
        print("Success rate: ", 1.0 * success_attack / total_cnt)
        print("Successful items count: ", success_attack)
        print("Total count: ", total_cnt)
        print("Index: ", index)
        print()
    #--------------------------------------------------------------------------------------------
    file_name = './advs/adv_t5_ours_ensemble.txt'
    with open(file_name, 'w') as f:
        for example in adv_example:
            f.write(example)
    print('file saved at {}!'.format(file_name))
    #--------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
