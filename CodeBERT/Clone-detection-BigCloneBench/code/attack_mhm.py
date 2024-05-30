from pickle import NONE
import torch
import sys
import os

sys.path.append('../../../')
sys.path.append('../../../python_parser')

import argparse
import warnings
import torch
from model import Model, Model_sub
from utils import set_seed
from utils import Recorder
from run import TextDataset ,convert_examples_to_features
from utils import CodeDataset
from attacker_crossdomain import MHM_Attacker
from run_parser import get_identifiers, get_example
from transformers import RobertaForMaskedLM
from transformers import (RobertaConfig, RobertaModel, RobertaTokenizer)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.simplefilter(action='ignore', category=FutureWarning) # Only report warning

MODEL_CLASSES = {
    'roberta': (RobertaConfig, RobertaModel, RobertaTokenizer)
}

from utils import build_vocab

def get_code_pairs(file_path):
    postfix=file_path.split('/')[-1].split('.txt')[0]
    folder = '/'.join(file_path.split('/')[:-1]) # 得到文件目录
    code_pairs_file_path = os.path.join(folder, 'cached_{}.pkl'.format(
                                    postfix))
    with open(code_pairs_file_path, 'rb') as f:
        code_pairs = pickle.load(f)
    return code_pairs
      
if __name__ == "__main__":
    
    import json
    import pickle
    import time
    import os
    
    # import tree as Tree
    # from dataset import Dataset, POJ104_SEQ
    # from lstm_classifier import LSTMEncoder, LSTMClassifier
    
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
                    
    parser.add_argument("--model_type", default="bert", type=str,
                        help="The model architecture to be fine-tuned.")
    parser.add_argument("--model_name_or_path", default=None, type=str,
                        help="The model checkpoint for weights initialization.")

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
    parser.add_argument("--block_size", default=-1, type=int,
                        help="Optional input sequence length after tokenization."
                             "The training dataset will be truncated in block of this size for training."
                             "Default to the model max input length for single sentence inputs (take into account special tokens).")
    parser.add_argument("--do_eval", action='store_true',
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--do_test", action='store_true',
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--original", action='store_true',
                        help="Whether to MHM original.")   
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

    codebert_mlm = RobertaForMaskedLM.from_pretrained(args.base_model)
    tokenizer_mlm = RobertaTokenizer.from_pretrained(args.base_model)

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


    checkpoint_prefix = 'checkpoint-best-f1/model.bin'
    output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
    model.load_state_dict(torch.load(output_dir))
    model.to(args.device)
    print ("MODEL LOADED!")
    codebert_mlm.to('cuda')

    model_sub = Model_sub(RobertaModel.from_pretrained('microsoft/codebert-base'), args=args)
    model_sub.to(args.device)

    # Load Dataset
    ## Load Dataset
    eval_dataset = TextDataset(tokenizer, args,args.eval_data_file)

    ## Load code pairs
    source_codes = get_code_pairs(args.eval_data_file)
    
    postfix = args.eval_data_file.split('/')[-1].split('.txt')[0].split("_")
    folder = '/'.join(args.eval_data_file.split('/')[:-1]) # 得到文件目录
    subs_path = os.path.join(folder, 'test_subs_baseline_{}_{}.jsonl'.format(
                                    postfix[-2], postfix[-1]))
    substitutes = []
    with open(subs_path) as f:
        for line in f:
            js = json.loads(line.strip())
            substitutes.append(js["substitutes"])
    assert len(source_codes) == len(eval_dataset) == len(substitutes)

    code_tokens = []
    for index, code in enumerate(source_codes):
        code_tokens.append(get_identifiers(code[2], "java")[1])


    # recoder = Recorder(args.csv_store_path)
    attacker = MHM_Attacker(args, model_sub, model, codebert_mlm, tokenizer, tokenizer_mlm)

    print ("ATTACKER BUILT!")
    
    adv = {"tokens": [], "raw_tokens": [], "ori_raw": [],
           'ori_tokens': [], "label": [], }
    success_attack = 0
    total_cnt = 0
    query_times = 0
    all_start_time = time.time()
    adv_example = []
    for index, example in enumerate(eval_dataset):
        example_start_time = time.time()
        code_pair = source_codes[index]
        substitute = substitutes[index]
        ground_truth = example[1].item()

        #打印clean样本
        print("idx_1: ", code_pair[0])
        print("clean code:\n", code_pair[2])
        
        # 这里需要进行修改.
        _res = attacker.mcmc(example, substitute, tokenizer, code_pair,
                            _label=ground_truth, _n_candi=30,
                            _max_iter=10, _prob_threshold=1)
        adv_code = _res['adv_code']
        is_success = _res['succ']

        example_end_time = (time.time()-example_start_time)/60
        print("Example time cost: ", round(example_end_time, 2), "min")
        print("ALL examples time cost: ", round((time.time()-all_start_time)/60, 2), "min")


        # recoder.writemhm(index, "CODE1: "+ code_pair[2].replace("\n", " ")+" ||CODE2: "+ code_pair[3].replace("\n", " "), _res["prog_length"], " ".join(_res['tokens']), ground_truth, _res["orig_label"], _res["new_pred"], _res["is_success"], _res["old_uid"], _res["score_info"], _res["nb_changed_var"], _res["nb_changed_pos"], _res["replace_info"], _res["attack_type"], model.query - query_times, time_cost)
        query_times = model.query

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
    with open('adv_codebert_mhm_untargeted.txt', 'w') as f:
        for example in adv_example:
            f.write(example)
    #--------------------------------------------------------------------------------------------