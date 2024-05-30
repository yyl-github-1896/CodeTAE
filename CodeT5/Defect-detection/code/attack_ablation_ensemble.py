
'''For attacking CodeT5 models'''
import sys
import os
import re

sys.path.append('../../../')
sys.path.append('../../../python_parser')
retval = os.getcwd()

import csv
import copy
import json
import logging
import argparse
import warnings
import torch
import torch.nn as nn
import numpy as np

from attacker_crossdomain import CrossDomainAttacker
from model import CodeT5
from run import set_seed
from run import TextDataset
from run import InputFeatures
from utils import is_valid_variable_name, _tokenize
from utils import get_identifier_posistions_from_code
from utils import get_masked_code_by_position
from run_parser import get_identifiers

from torch.utils.data.dataset import Dataset
from torch.utils.data import SequentialSampler, DataLoader
from transformers import RobertaForMaskedLM
from transformers import (T5Config, T5ForConditionalGeneration, RobertaTokenizer, RobertaModel)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.simplefilter(action='ignore', category=FutureWarning) # Only report warning\

MODEL_CLASSES = {
    't5': (T5Config, T5ForConditionalGeneration, RobertaTokenizer),
}

logger = logging.getLogger(__name__)


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
    parser.add_argument("--eval_data_file_2", default=None, type=str,
                        help="An optional input evaluation data file to evaluate the perplexity on (a text file).")
    parser.add_argument("--test_data_file", default=None, type=str,
                        help="An optional input evaluation data file to evaluate the perplexity on (a text file).")

    parser.add_argument("--model_type", default="bert", type=str,
                        help="The model architecture to be fine-tuned.")
    parser.add_argument("--model_name_or_path", default=None, type=str,
                        help="The model checkpoint for weights initialization.")

    # Hyper-parameters
    parser.add_argument("--num_of_changes", required=True, type=int,
                        help="number of inserted obfuscations.")

    parser.add_argument("--base_model", default=None, type=str,
                        help="Base Model")
    parser.add_argument("--csv_store_path", default=None, type=str,
                        help="Base Model")

    parser.add_argument("--mlm", action='store_true',
                        help="Train with masked-language modeling loss instead of language modeling.")
    parser.add_argument("--mlm_probability", type=float, default=0.15,
                        help="Ratio of tokens to mask for masked language modeling loss")

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
    parser.add_argument("--do_lower_case", action='store_true',
                        help="Set this flag if you are using an uncased model.")

    parser.add_argument("--train_batch_size", default=4, type=int,
                        help="Batch size per GPU/CPU for training.")
    parser.add_argument("--eval_batch_size", default=4, type=int,
                        help="Batch size per GPU/CPU for evaluation.")
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1,
                        help="Number of updates steps to accumulate before performing a backward/update pass.")
    parser.add_argument("--learning_rate", default=5e-5, type=float,
                        help="The initial learning rate for Adam.")
    parser.add_argument("--weight_decay", default=0.0, type=float,
                        help="Weight deay if we apply some.")
    parser.add_argument("--adam_epsilon", default=1e-8, type=float,
                        help="Epsilon for Adam optimizer.")
    parser.add_argument("--max_grad_norm", default=1.0, type=float,
                        help="Max gradient norm.")
    parser.add_argument("--num_train_epochs", default=1.0, type=float,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--max_steps", default=-1, type=int,
                        help="If > 0: set total number of training steps to perform. Override num_train_epochs.")
    parser.add_argument("--warmup_steps", default=0, type=int,
                        help="Linear warmup over warmup_steps.")

    parser.add_argument('--logging_steps', type=int, default=50,
                        help="Log every X updates steps.")
    parser.add_argument('--save_steps', type=int, default=50,
                        help="Save checkpoint every X updates steps.")
    parser.add_argument('--save_total_limit', type=int, default=None,
                        help='Limit the total amount of checkpoints, delete the older checkpoints in the output_dir, does not delete by default')
    parser.add_argument("--eval_all_checkpoints", action='store_true',
                        help="Evaluate all checkpoints starting with the same prefix as model_name_or_path ending and ending with step number")
    parser.add_argument("--no_cuda", action='store_true',
                        help="Avoid using CUDA when available")
    parser.add_argument('--overwrite_output_dir', action='store_true',
                        help="Overwrite the content of the output directory")
    parser.add_argument('--overwrite_cache', action='store_true',
                        help="Overwrite the cached training and evaluation sets")
    parser.add_argument('--seed', type=int, default=42,
                        help="random seed for initialization")
    parser.add_argument('--epoch', type=int, default=42,
                        help="random seed for initialization")
    parser.add_argument('--fp16', action='store_true',
                        help="Whether to use 16-bit (mixed) precision (through NVIDIA apex) instead of 32-bit")
    parser.add_argument('--fp16_opt_level', type=str, default='O1',
                        help="For fp16: Apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']."
                             "See details at https://nvidia.github.io/apex/amp.html")
    parser.add_argument("--local_rank", type=int, default=-1,
                        help="For distributed training: local_rank")
    parser.add_argument('--server_ip', type=str, default='', help="For distant debugging.")
    parser.add_argument('--server_port', type=str, default='', help="For distant debugging.")


    args = parser.parse_args()


    args.device = torch.device("cuda")
    # Set seed
    set_seed(args.seed)


    args.start_epoch = 0
    args.start_step = 0


    ## Load Target Model
    checkpoint_last = os.path.join(args.output_dir, 'checkpoint-last') # 读取model的路径
    if os.path.exists(checkpoint_last) and os.listdir(checkpoint_last):
        # 如果路径存在且有内容，则从checkpoint load模型
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
    config.num_labels=1
    tokenizer = RobertaTokenizer.from_pretrained('../cache/Salesforce/codet5-base/')

    if args.block_size <= 0:
        args.block_size = tokenizer.max_len_single_sentence  # Our input block size will be the max possible for the model
    args.block_size = min(args.block_size, tokenizer.max_len_single_sentence)

    if args.model_name_or_path:
        model_tgt = model_class.from_pretrained('../cache/Salesforce/codet5-base/')    
    else:
        model_tgt = model_class(config)

    model_tgt = CodeT5(model_tgt,config,tokenizer,args).to(args.device)

    checkpoint_prefix = 'checkpoint-best-acc/model.bin'
    output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
    ckpt = torch.load(output_dir)
    model_tgt.load_state_dict(torch.load(output_dir))
    model_tgt.to(args.device)

    try:
        model_sub = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-base").to(args.device)
    except:
        model_sub = T5ForConditionalGeneration.from_pretrained('../cache/Salesforce/codet5-base/').to(args.device)


    ## Load CodeBERT (MLM) model
    tokenizer_mlm = tokenizer

    ## Load Dataset
    test_dataset = TextDataset(tokenizer, args,args.eval_data_file)

    source_codes = []
    with open(args.eval_data_file) as f:
        for line in f:
            js=json.loads(line.strip())
            code = ' '.join(js['func'].split())
            source_codes.append(code)
    assert(len(source_codes) == len(test_dataset))


    '''***********************************switch substitutes here*********************************'''
    substitutes = []
    with open(args.eval_data_file) as f:
        for line in f:
            js = json.loads(line.strip())
            substitutes.append(js["substitutes"])
    assert len(source_codes) == len(test_dataset) == len(substitutes)


    '''***********************************add another subs dataset here*********************************'''
    substitutes_2 = []
    with open(args.eval_data_file_2) as f:
        for line in f:
            js = json.loads(line.strip())
            substitutes_2.append(js["substitutes"])
    assert len(source_codes) == len(test_dataset) == len(substitutes)

    # 现在要尝试计算importance_score了.
    success_attack = 0
    total_cnt = 0
    f = open(args.csv_store_path, 'w')
    
    writer = csv.writer(f)
    # write table head.
    writer.writerow(["Original Code", 
                    "Program Length", 
                    "Adversarial Code", 
                    "True Label", 
                    "Original Prediction", 
                    "Adv Prediction", 
                    "Is Success", 
                    "Extracted Names",
                    "Importance Score",
                    "No. Changed Names",
                    "No. Changed Tokens",
                    "Replaced Names"])

    attacker = CrossDomainAttacker(args, model_sub, model_tgt, tokenizer, tokenizer)
    adv_example = []
    for index, example in enumerate(test_dataset):
        # if index >= 400:
        #     break

        code = source_codes[index]
        subs = substitutes[index]
        subs_2 = substitutes_2[index]

        code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example, code, subs)
        if is_success == -1:
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example, code, subs_2)
        
        code_after_greedy = adv_code
        if is_success == -1: #
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.insert_attack(example, code_after_greedy, subs)
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.insert_attack(example, code_after_greedy, subs_2)
        
        code_after_insert = adv_code
        if is_success == -1: #
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.empty_print_attack(example, code_after_insert, subs)
        
        code_after_print = adv_code
        if is_success == -1: #
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example, code_after_print, subs)
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example, code_after_print, subs_2)
        
        code_after_if = adv_code
        if is_success == -1: #
            attacker.args.num_of_changes = 4
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example, code_after_if, subs)
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example, code_after_if, subs_2)


        score_info = ''
        replace_info = ''

        writer.writerow([code, 
                        prog_length, 
                        adv_code, 
                        true_label, 
                        orig_label, 
                        temp_label, 
                        is_success, 
                        ",".join(variable_names),
                        score_info,
                        nb_changed_var,
                        nb_changed_pos,
                        replace_info])

        #--------------------------------------------------------------------------------------------
        adv_code_lines = [x + '\\n' for x in adv_code.split('\n') if x ]
        new_content = "".join(adv_code_lines) + '\n'
        adv_example.append(new_content)
        print(new_content)
        #--------------------------------------------------------------------------------------------
        
        if is_success >= -1 :
            # 如果原来正确
            total_cnt += 1
        if is_success == 1:
            success_attack += 1
            print("Succeed!")
        elif is_success == -4:
            print("Wrong prediction.")
        elif is_success == -3:
            print("No variable names!")
        else:
            print("Failed!")
        
        if total_cnt == 0:
            continue
        print("Success rate: ", 1.0 * success_attack / total_cnt)
        print("Successful items count: ", success_attack)
        print("Total count: ", total_cnt)
        print("Index: ", index)
        print('='*100)
    #--------------------------------------------------------------------------------------------
    file_name = './adv_t5_ablation_ensemble2.txt'
    with open(file_name, 'w') as f:
        for example in adv_example:
            f.write(example)
    print('file saved at {}!'.format(file_name))

    # num = 0
    # js_all=json.load(open('../preprocess/function.json'))
    # train_index=set()
    # with open('../preprocess/train.txt') as f:
    #     for line in f:
    #         line=line.strip()
    #         train_index.add(int(line))

    # with open('./train_400_t5_adv.jsonl','w') as f:
    #     for idx,js in enumerate(js_all):
    #         if idx in train_index:
    #             js['idx']=idx
    #             js["func"]=adv_example[num]
    #             f.write(json.dumps(js)+'\n')
    #             num += 1
    #             if num >= 400:
    #                 break
    #--------------------------------------------------------------------------------------------
    
        
if __name__ == '__main__':
    main()