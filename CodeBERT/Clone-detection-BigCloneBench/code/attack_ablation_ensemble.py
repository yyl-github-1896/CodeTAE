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

from model import Model, Model_sub
from utils import set_seed
from utils import Recorder
from run import TextDataset
from attacker_crossdomain import CrossDomainAttacker
from transformers import RobertaForMaskedLM
from transformers import (RobertaConfig, RobertaModel, RobertaTokenizer)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.simplefilter(action='ignore', category=FutureWarning) # Only report warning

MODEL_CLASSES = {
    'roberta': (RobertaConfig, RobertaModel, RobertaTokenizer)
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

    # Hyper-papameters
    parser.add_argument("--num_of_changes", type=int, required=True,
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
    config = config_class.from_pretrained(args.config_name if args.config_name else args.model_name_or_path,
                                          cache_dir=args.cache_dir if args.cache_dir else None)
    config.num_labels=2
    tokenizer = tokenizer_class.from_pretrained(args.tokenizer_name,
                                                do_lower_case=False,
                                                cache_dir=args.cache_dir if args.cache_dir else None)
    if args.block_size <= 0:
        args.block_size = tokenizer.max_len_single_sentence  # Our input block size will be the max possible for the model
    args.block_size = min(args.block_size, tokenizer.max_len_single_sentence)
    if args.model_name_or_path:
        model = model_class.from_pretrained(args.model_name_or_path,
                                            from_tf=bool('.ckpt' in args.model_name_or_path),
                                            config=config,
                                            cache_dir=args.cache_dir if args.cache_dir else None)    
    else:
        model = model_class(config)

    model=Model(model,config,tokenizer,args)


    checkpoint_prefix = 'checkpoint-best-f1/model.bin'
    output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
    model.load_state_dict(torch.load(output_dir))
    model.to(args.device)

    model_sub = Model_sub(RobertaModel.from_pretrained('microsoft/codebert-base'), args=args)
    model_sub.to(args.device)

    ## Load CodeBERT (MLM) model
    codebert_mlm = RobertaForMaskedLM.from_pretrained(args.base_model)
    tokenizer_mlm = RobertaTokenizer.from_pretrained(args.base_model)
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

    '''***********************************switch substitutes here*********************************'''
    subs_path = os.path.join(folder, 'test_subs_gan_{}_{}.jsonl'.format(
                                    postfix[-2], postfix[-1]))
    substitutes_2 = []
    with open(subs_path) as f:
        for line in f:
            js = json.loads(line.strip())
            substitutes_2.append(js["substitutes"])
    assert len(source_codes) == len(eval_dataset) == len(substitutes_2)


    # 现在要尝试计算importance_score了.
    success_attack = 0
    total_cnt = 0

    recoder = Recorder(args.csv_store_path)
    attacker = CrossDomainAttacker(args, model_sub, model, tokenizer, codebert_mlm, tokenizer_mlm, use_bpe=1, threshold_pred_score=0)
    start_time = time.time()
    query_times = 0
    #--------------------------------------------------------------------------------------------
    # url_to_code={}
    # with open('../dataset/data.jsonl') as f:
    #     for line in f:
    #         line=line.strip()
    #         js=json.loads(line)
    #         url_to_code[js['idx']]=js['func']
    #--------------------------------------------------------------------------------------------
    attack_type_list = ['identifier_renaming', 'insert_unused_variable', 'insert_empty_print', 'insert_empty_if', 'insert_empty_while']
    adv_example = []
    for index, example in enumerate(eval_dataset):
        example_start_time = time.time()
        code_pair = source_codes[index]
        substitute = substitutes[index]
        substitute_2 = substitutes_2[index]
        #打印clean样本
        print("idx_1: ", code_pair[0])
        print("clean code:\n", code_pair[2])


        if 'identifier_renaming' in attack_type_list:
            #substitute
            args.num_of_changes = 2
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example, substitute, code_pair)
            #substitute_2
            if is_success == -1:
                args.num_of_changes = 2
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example, substitute_2, code)
        
        if 'insert_unused_variable' in attack_type_list:
            ours_code = adv_code
            if is_success == -1:
                args.num_of_changes = 6
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.insert_attack(example, substitute, code, adv=ours_code)
                if is_success == -1:
                    args.num_of_changes = 6
                    code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.insert_attack(example, substitute_2, code, adv=ours_code)

        # if 'insert_empty_print' in attack_type_list:
        #     ours_insert_code = adv_code
        #     if is_success == -1:
        #         code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.empty_print_attack(example,  substitute, code, adv=ours_insert_code)

        if 'insert_empty_if' in attack_type_list:
            ours_insert_print_code = adv_code
            if is_success == -1:
                args.num_of_changes = 15
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example,  substitute, code, adv=ours_insert_print_code)
                if is_success == -1:
                    args.num_of_changes = 15
                    code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example,  substitute_2, code, adv=ours_insert_print_code)

        if 'insert_empty_while' in attack_type_list:
            ours_insert_print_if_code = adv_code
            if is_success == -1:
                args.num_of_changes = 15
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example,  substitute, code, adv=ours_insert_print_if_code)
                if is_success == -1:
                    args.num_of_changes = 15
                    code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example,  substitute_2, code, adv=ours_insert_print_if_code)

        example_end_time = (time.time()-example_start_time)/60
        
        print("Example time cost: ", round(example_end_time, 2), "min")
        print("ALL examples time cost: ", round((time.time()-start_time)/60, 2), "min")

        # score_info = ''
        # if names_to_importance_score is not None:
        #     for key in names_to_importance_score.keys():
        #         score_info += key + ':' + str(names_to_importance_score[key]) + ','

        # replace_info = ''
        # if replaced_words is not None:
        #     for key in replaced_words.keys():
        #         replace_info += key + ':' + replaced_words[key] + ','
        # print("Query times in this attack: ", model.query - query_times)
        # print("All Query times: ", model.query)

        # recoder.write(index, code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, score_info, nb_changed_var, nb_changed_pos, replace_info, attack_type, model.query - query_times, example_end_time)
        
        # query_times = model.query

        #打印adv样本
        print("adv code:\n", adv_code)
        adv_code_lines = [x + '\\n' for x in adv_code.split('\n') if x ]
        adv_code_save = "".join(adv_code_lines)
        adv_code_save = adv_code_save + '\n'
        print(adv_code_save)
        adv_example.append(adv_code_save)

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
        print('='*100)
    
    #--------------------------------------------------------------------------------------------
    with open('adv_codebert_ablation_ensemble.txt', 'w') as f:
        for example in adv_example:
            f.write(example)
    #--------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()