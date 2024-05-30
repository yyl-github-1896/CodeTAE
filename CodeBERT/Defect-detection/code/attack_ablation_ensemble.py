'''For attacking CodeBERT models'''
import sys
import os

sys.path.append('../../../')
sys.path.append('../../../python_parser')

import json
import logging
import argparse
import warnings
import torch
import time
from model import Model
from run import TextDataset
from utils import set_seed
from python_parser.parser_folder import remove_comments_and_docstrings
from utils import Recorder
from attacker_crossdomain import CrossDomainAttacker
from transformers import (RobertaForMaskedLM, RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer, RobertaModel)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.simplefilter(action='ignore', category=FutureWarning) # Only report warning

MODEL_CLASSES = {
    'roberta': (RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer)
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

    parser.add_argument("--base_model", default=None, type=str,
                        help="Base Model")
    parser.add_argument("--csv_store_path", default=None, type=str,
                        help="Path to store the CSV file")

    # Hyper-parameters
    parser.add_argument("--num_of_changes", required=True, type=int,
                        help="number of changes")

    parser.add_argument("--mlm", action='store_true',
                        help="Train with masked-language modeling loss instead of language modeling.")
    parser.add_argument("--mlm_probability", type=float, default=0.15,
                        help="Ratio of tokens to mask for masked language modeling loss")

    parser.add_argument("--config_name", default="", type=str,
                        help="Optional pretrained config name or path if not the same as model_name_or_path")
    parser.add_argument("--tokenizer_name", default="", type=str,
                        help="Optional pretrained tokenizer name or path if not the same as model_name_or_path")
    parser.add_argument("--block_size", default=-1, type=int,
                        help="Optional input sequence length after tokenization."
                             "The training dataset will be truncated in block of this size for training."
                             "Default to the model max input length for single sentence inputs (take into account special tokens).")
    parser.add_argument("--do_train", action='store_true',
                        help="Whether to run training.")
    parser.add_argument("--use_ga", action='store_true',
                        help="Whether to GA-Attack.")
    parser.add_argument("--do_eval", action='store_true',
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--do_test", action='store_true',
                        help="Whether to run eval on the dev set.")    
    parser.add_argument("--eval_batch_size", default=4, type=int,
                        help="Batch size per GPU/CPU for evaluation.")
    parser.add_argument('--seed', type=int, default=42,
                        help="random seed for initialization")
    parser.add_argument("--cache_dir", default="", type=str,
                        help="Optional directory to store the pre-trained models downloaded from s3 (instread of the default one)")



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
    config = config_class.from_pretrained(args.config_name if args.config_name else args.model_name_or_path,
                                          cache_dir=args.cache_dir if args.cache_dir else None)
    config.num_labels=1 # 只有一个label?
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

    model = Model(model,config,tokenizer,args)


    checkpoint_prefix = 'checkpoint-best-acc/model.bin'
    output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
    model.load_state_dict(torch.load(output_dir))      
    model.to(args.device)

    model_sub = RobertaModel.from_pretrained('microsoft/codebert-base').to(args.device)

    ## Load CodeBERT (MLM) model
    codebert_mlm = RobertaForMaskedLM.from_pretrained(args.base_model)
    tokenizer_mlm = RobertaTokenizer.from_pretrained(args.base_model)
    codebert_mlm.to('cuda') 

    ## Load Dataset
    eval_dataset = TextDataset(tokenizer, args,args.eval_data_file)

    # Load original source codes
    source_codes = []
    '''***********************************switch substitutes here*********************************'''
    subs = []
    with open(args.eval_data_file) as f:
        for line in f:
            js=json.loads(line.strip())
            code = js['func']
            source_codes.append(code)
            subs.append(js['substitutes'])
    assert(len(source_codes) == len(eval_dataset) == len(subs))

    '''***********************************add another subs dataset here*********************************'''
    subs_2 = []
    with open(args.eval_data_file_2) as f:
        for line in f:
            js=json.loads(line.strip())
            subs_2.append(js['substitutes'])
    assert(len(source_codes) == len(eval_dataset) == len(subs_2)) 

    success_attack = 0
    total_cnt = 0

    recoder = Recorder(args.csv_store_path)
    attacker = CrossDomainAttacker(args, model_sub, model, tokenizer, codebert_mlm, tokenizer_mlm)
    start_time = time.time()
    query_times = 0
    attack_type_list = ['identifier_renaming', 'insert_unused_variable', 'insert_empty_print', 'insert_empty_if', 'insert_empty_while']
    adv_example = []
    for index, example in enumerate(eval_dataset):
        example_start_time = time.time()
        code = source_codes[index]
        sub = subs[index]
        sub_2 = subs_2[index]
        #打印clean样本
        # print("clean code:\n", code)
        
        if 'identifier_renaming' in attack_type_list:
            #subs
            attacker.args.num_of_changes = 2
            code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example, code, sub)
            #subs_2
            if is_success == -1:
                attacker.args.num_of_changes = 2
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.greedy_attack(example, code, sub_2)

        if 'insert_unused_variable' in attack_type_list:
            ours_code = adv_code
            if is_success == -1:
                attacker.args.num_of_changes = 2
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.insert_attack(example, ours_code, sub)
                if is_success == -1:
                    attacker.args.num_of_changes = 2
                    code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.insert_attack(example, ours_code, sub_2)

        if 'insert_empty_print' in attack_type_list:
            ours_insert_code = adv_code
            if is_success == -1:
                attacker.args.num_of_changes = 2
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.empty_print_attack(example, ours_insert_code, sub)

        if 'insert_empty_if' in attack_type_list:
            ours_insert_print_code = adv_code
            if is_success == -1:
                attacker.args.num_of_changes = 2
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example, ours_insert_print_code, sub)
                if is_success == -1:
                    attacker.args.num_of_changes = 2
                    code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_if_attack(example, ours_insert_print_code, sub_2)

        if 'insert_empty_while' in attack_type_list:
            ours_insert_print_if_code = adv_code
            attacker.args.num_of_changes = 4
            if is_success == -1:
                code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example, ours_insert_print_if_code, sub)
                if is_success == -1:
                    attacker.args.num_of_changes = 4
                    code, prog_length, adv_code, true_label, orig_label, temp_label, is_success, variable_names, names_to_importance_score, nb_changed_var, nb_changed_pos, replaced_words = attacker.nonreachable_while_attack(example, ours_insert_print_if_code, sub_2)


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
        # print("adv code:\n", adv_code)
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
    with open('./adv_codebert_ensemble_train.txt', 'w') as f:
        for example in adv_example:
            f.write(example)

    num = 0
    js_all=json.load(open('../preprocess/function.json'))
    train_index=set()
    with open('../preprocess/train.txt') as f:
        for line in f:
            line=line.strip()
            train_index.add(int(line))

    with open('./train_adv.jsonl','w') as f:
        for idx,js in enumerate(js_all):
            if idx in train_index:
                js['idx']=idx
                js["func"]=adv_example[num]
                f.write(json.dumps(js)+'\n')
                num += 1
                if num >= 4000:
                    break
    
        
if __name__ == '__main__':
    main()