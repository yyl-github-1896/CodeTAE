
'''For attacking CodeBERT models'''
import sys
import os

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
import numpy as np
import pickle
import time
from run import convert_examples_to_features
from run import set_seed
from run import TextDataset
from run import InputFeatures
from utils import Recorder
from utils import python_keywords, is_valid_substitute, _tokenize
from utils import get_identifier_posistions_from_code
from utils import get_masked_code_by_position, get_substitutes, is_valid_variable_name
from model import Model, Model_sub
from run_parser import get_code_tokens
from attacker_crossdomain import CrossDomainAttacker

from torch.utils.data.dataset import Dataset
from torch.utils.data import SequentialSampler, DataLoader
from transformers import RobertaForMaskedLM
from transformers import (RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TRANSFORMERS_OFFLINE'] = '1'   # run the code in offline mode
warnings.simplefilter(action='ignore', category=FutureWarning) # Only report warning

MODEL_CLASSES = {
    'roberta': (RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer),
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
    parser.add_argument("--eval_target_file", default=None, type=str,
                        help="Target label for targeted attack on valid dataset.")
    parser.add_argument("--test_data_file", default=None, type=str,
                        help="An optional input evaluation data file to evaluate the perplexity on (a text file).")
                    
    parser.add_argument("--model_type", default="bert", type=str,
                        help="The model architecture to be fine-tuned.")
    parser.add_argument("--model_name_or_path", default=None, type=str,
                        help="The model checkpoint for weights initialization.")
    parser.add_argument("--csv_store_path", type=str,
                        help="Path to store the CSV file")

    parser.add_argument("--config_name", default="", type=str,
                        help="Optional pretrained config name or path if not the same as model_name_or_path")
    parser.add_argument("--tokenizer_name", default="", type=str,
                        help="Optional pretrained tokenizer name or path if not the same as model_name_or_path")
    parser.add_argument("--cache_dir", default="", type=str,
                        help="Optional directory to store the pre-trained models downloaded from s3 (instread of the default one)")
    parser.add_argument("--code_length", default=256, type=int,
                        help="Optional input sequence length after tokenization."
                             "The training dataset will be truncated in block of this size for training."
                             "Default to the model max input length for single sentence inputs (take into account special tokens).")
    parser.add_argument("--data_flow_length", default=64, type=int,
                        help="Optional input sequence length after tokenization.")
    parser.add_argument("--do_train", action='store_true',
                        help="Whether to run training.")
    parser.add_argument("--do_eval", action='store_true',
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--do_test", action='store_true',
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--language_type", type=str,
                        help="The programming language type of dataset")     
    parser.add_argument("--evaluate_during_training", action='store_true',
                        help="Run evaluation during training at each logging step.")
    parser.add_argument("--do_lower_case", action='store_true',
                        help="Set this flag if you are using an uncased model.")
    parser.add_argument("--number_labels", type=int,
                        help="The model checkpoint for weights initialization.")
    parser.add_argument("--train_batch_size", default=4, type=int,
                        help="Batch size per GPU/CPU for training.")
    parser.add_argument("--eval_batch_size", default=4, type=int,
                        help="Batch size per GPU/CPU for evaluation.")

    # Hyper-parameters
    parser.add_argument("--num_of_changes", required=True, type=int,
                        help="number of inserted obfuscations.")

    parser.add_argument('--seed', type=int, default=42,
                        help="random seed for initialization")


    args = parser.parse_args()

    args.n_gpu = torch.cuda.device_count()
    args.device = torch.device("cuda")
    # Set seed
    set_seed(args)


    args.start_epoch = 0
    args.start_step = 0


    ## Load Target Model
    checkpoint_last = os.path.join(args.output_dir, 'checkpoint-last') # 读取model的路径
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
    try:
        config = config_class.from_pretrained(args.config_name if args.config_name else args.model_name_or_path,
                                          cache_dir=args.cache_dir if args.cache_dir else None)
    except:
        config = config_class.from_pretrained('../cache/microsoft/graphcodebert-base/config.json')
    config.num_labels=args.number_labels # 只有一个label?
    try:
        tokenizer = tokenizer_class.from_pretrained(args.tokenizer_name,
                                                do_lower_case=args.do_lower_case,
                                                cache_dir=args.cache_dir if args.cache_dir else None)
    except:
        tokenizer = tokenizer_class.from_pretrained('../cache/microsoft/graphcodebert-base/')
    # if args.block_size <= 0:
    #     args.block_size = tokenizer.max_len_single_sentence  # Our input block size will be the max possible for the model
    # args.block_size = min(args.block_size, tokenizer.max_len_single_sentence)
    if args.model_name_or_path:
        try:
            model_tgt = model_class.from_pretrained(args.model_name_or_path,
                                            from_tf=bool('.ckpt' in args.model_name_or_path),
                                            config=config,
                                            cache_dir=args.cache_dir if args.cache_dir else None)    
        except:
            model_tgt = model_class.from_pretrained('../cache/microsoft/graphcodebert-base/')
    else:
        model_tgt = model_class(config)

    model_tgt = Model(model_tgt,config,tokenizer,args).to(args.device)


    checkpoint_prefix = 'checkpoint-best-acc/model.bin'
    output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
    model_tgt.load_state_dict(torch.load(output_dir))      


    model_sub = Model_sub(RobertaForSequenceClassification.from_pretrained("microsoft/graphcodebert-base")).to(args.device)


    ## Load CodeBERT (MLM) model
    try:
        codebert_mlm = RobertaForMaskedLM.from_pretrained("microsoft/graphcodebert-base")
    except:
        codebert_mlm = RobertaForMaskedLM.from_pretrained("../cache/microsoft/graphcodebert-base/")
    try:
        tokenizer_mlm = RobertaTokenizer.from_pretrained("microsoft/graphcodebert-base")
    except:
        tokenizer_mlm = RobertaTokenizer.from_pretrained("../cache/microsoft/graphcodebert-base/")
    codebert_mlm.to('cuda') 

    ## Load Dataset
    eval_dataset = TextDataset(tokenizer, args, args.eval_data_file)
    if args.eval_target_file is not None:
        target_dataset = TextDataset(tokenizer, args, args.eval_target_file)

    file_type = args.eval_data_file.split('/')[-1].split('.')[0] # valid
    folder = '/'.join(args.eval_data_file.split('/')[:-1]) # 得到文件目录
    # codes_file_path = os.path.join(folder, '{}_subs.jsonl'.format(
    #                             file_type))
    '''***********************************switch substitutes here*********************************'''
    codes_file_path = os.path.join(folder, '{}_subs.jsonl'.format(
                                file_type))
    print(codes_file_path)
    source_codes = []
    substs = []
    with open(codes_file_path) as rf:
        for line in rf:
            item = json.loads(line.strip())
            source_codes.append(item["code"].replace("\\n", "\n").replace('\"','"'))
            substs.append(item["substitutes"])
    print('len(source_code): {}, len(eval_dataset): {}, len(substs): {}'.format(len(source_codes), len(eval_dataset), len(substs)))
    assert(len(source_codes) == len(eval_dataset) == len(substs))


    '''***********************************add another subs dataset here*********************************'''
    codes_file_path = os.path.join(folder, '{}_subs_gan.jsonl'.format(
                                file_type))
    print(codes_file_path)
    source_codes = []
    substs_2 = []
    with open(codes_file_path) as rf:
        for line in rf:
            item = json.loads(line.strip())
            source_codes.append(item["code"].replace("\\n", "\n").replace('\"','"'))
            substs_2.append(item["substitutes"])


    success_attack = 0
    total_cnt = 0
    recoder = Recorder(args.csv_store_path)
    attacker = CrossDomainAttacker(args, model_sub, model_tgt, tokenizer, codebert_mlm, tokenizer_mlm, use_bpe=1, threshold_pred_score=0)
    start_time = time.time()
    query_times = 0
    adv_example = []
    for index, (example_eval) in enumerate(eval_dataset):
        example = example_eval

        example_start_time = time.time()
        code = source_codes[index]
        subs = substs[index]
        subs_2 = substs_2[index]
        
        is_success = -1
        if is_success == -1:
            attacker.args.num_of_changes = 2
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example, code, subs)
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example, code, subs_2)

        adv_variable = adv_code
        if is_success == -1:
            attacker.args.num_of_changes = 4
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.insert_attack(example, adv_variable, subs)
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.insert_attack(example, adv_variable, subs_2)
        
        adv_variable_insert = adv_code
        if is_success == -1:
            attacker.args.num_of_changes = 2
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.empty_print_attack(example, adv_variable_insert, subs)
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.empty_print_attack(example, adv_variable_insert, subs_2)
        
        adv_variable_insert_print = adv_code
        if is_success == -1:
            attacker.args.num_of_changes = 2
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example, adv_variable_insert_print, subs)
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example, adv_variable_insert_print, subs_2)

        adv_variable_insert_print_if = adv_code
        if is_success == -1:
            attacker.args.num_of_changes = 2
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example, adv_variable_insert_print_if, subs)
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example, adv_variable_insert_print_if, subs_2)
        
        attack_type = "Greedy"

        example_end_time = (time.time()-example_start_time)/60
        
        print("Example time cost: ", round(example_end_time, 2), "min")
        print("ALL examples time cost: ", round((time.time()-start_time)/60, 2), "min")
        score_info = ''
        if names_to_importance_score is not None:
            for key in names_to_importance_score.keys():
                score_info += key + ':' + str(names_to_importance_score[key]) + ','

        replace_info = ''
        if replaced_words is not None:
            for key in replaced_words.keys():
                replace_info += key + ':' + replaced_words[key] + ','
        # recoder.write(index, code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, score_info, nb_changed_var, nb_changed_pos, replace_info, attack_type, 0, example_end_time)
        
        # print('type: ', type(adv_code)) #type:  <class 'str'>
        
        lines_after_removal = []
        for a_line in adv_code.splitlines(True):
            if  a_line.strip().startswith("import") or a_line.strip().startswith("#") or a_line.strip().startswith("from"):
                continue
            lines_after_removal.append(a_line)
        
        content = "".join(lines_after_removal)
        # print(content)
        code_tokens = get_code_tokens(content, 'python')
        content = "".join(code_tokens)
        new_content = content + ' <CODESPLIT> ' + str(example[3].item()) + '\n'
        adv_example.append(new_content)
        print(new_content)

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

    file_name = './adv_graphcodebert_ensemble_train.txt'
    with open(file_name, 'w') as f:
        for example in adv_example:
            f.write(example)


if __name__ == '__main__':
    main()