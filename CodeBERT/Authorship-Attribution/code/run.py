"""
Fine-tuning the library models for language modeling on a text file (GPT, GPT-2, BERT, RoBERTa).
GPT and GPT-2 are fine-tuned using a causal language modeling (CLM) loss while BERT and RoBERTa are fine-tuned
using a masked language modeling (MLM) loss.
"""

from __future__ import absolute_import, division, print_function
import sys
import argparse
import glob
import logging
import os
import pickle
import random
import re
import shutil
import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, SequentialSampler, RandomSampler,TensorDataset
from torch.utils.data.distributed import DistributedSampler
sys.path.append('../../../')
from GraphCodeBERT.AuthorshipAttribution.code.model import Model_sub as gcb_Model_sub

try:
    from torch.utils.tensorboard import SummaryWriter
except:
    from tensorboardX import SummaryWriter

from tqdm import tqdm, trange
import multiprocessing
from model import Model, Model_sub, Model_for_sim

cpu_cont = 16
from transformers import (WEIGHTS_NAME, AdamW, get_linear_schedule_with_warmup,
                          BertConfig, BertForMaskedLM, BertTokenizer,
                          GPT2Config, GPT2LMHeadModel, GPT2Tokenizer,
                          OpenAIGPTConfig, OpenAIGPTLMHeadModel, OpenAIGPTTokenizer,
                          RobertaConfig, RobertaModel, RobertaTokenizer, RobertaForSequenceClassification, T5ForConditionalGeneration,
                          DistilBertConfig, DistilBertForMaskedLM, DistilBertTokenizer)

logger = logging.getLogger(__name__)

MODEL_CLASSES = {
    'gpt2': (GPT2Config, GPT2LMHeadModel, GPT2Tokenizer),
    'openai-gpt': (OpenAIGPTConfig, OpenAIGPTLMHeadModel, OpenAIGPTTokenizer),
    'bert': (BertConfig, BertForMaskedLM, BertTokenizer),
    'roberta': (RobertaConfig, RobertaModel, RobertaTokenizer),
    'distilbert': (DistilBertConfig, DistilBertForMaskedLM, DistilBertTokenizer)
}


class InputFeatures(object):
    """A single training/test features for a example."""
    def __init__(self,
                 input_tokens,
                 input_ids,
                 idx,
                 label=None,

    ):
        self.input_tokens = input_tokens
        self.input_ids = input_ids
        self.idx=str(idx)
        self.label=label
        
def convert_examples_to_features(code, label, tokenizer,args):
    #source
    code_tokens=tokenizer.tokenize(code)[:args.block_size-2]
    source_tokens =[tokenizer.cls_token]+code_tokens+[tokenizer.sep_token]
    source_ids =  tokenizer.convert_tokens_to_ids(source_tokens)
    padding_length = args.block_size - len(source_ids)
    source_ids+=[tokenizer.pad_token_id]*padding_length
    return InputFeatures(source_tokens,source_ids,0,label)

class TextDataset(Dataset):
    def __init__(self, tokenizer, args, file_path=None):
        self.examples = []
        # To-Do: 这里需要根据code authorship的数据集重新做.
        file_type = file_path.split('/')[-1].split('.')[0]
        folder = '/'.join(file_path.split('/')[:-1]) # 得到文件目录

        cache_file_path = os.path.join(folder, 'cached_{}'.format(
                                    file_type))
        code_pairs_file_path = os.path.join(folder, 'cached_{}.pkl'.format(
                                    file_type))

        print('\n cached_features_file: ',cache_file_path)
        try:
            self.examples = torch.load(cache_file_path)
            with open(code_pairs_file_path, 'rb') as f:
                code_files = pickle.load(f)
            
            logger.info("Loading features from cached file %s", cache_file_path)
        
        except:
            logger.info("Creating features from dataset file at %s", file_path)
            code_files = []
            with open(file_path) as f:
                for line in f:
                    code = line.split(" <CODESPLIT> ")[0]
                    code = code.replace("\\n", "\n").replace('\"','"')
                    label = line.split(" <CODESPLIT> ")[1]
                    # 将这俩内容转化成input.
                    self.examples.append(convert_examples_to_features(code, int(label), tokenizer,args))
                    code_files.append(code)
                    # 这里每次都是重新读取并处理数据集，能否cache然后load
            assert(len(self.examples) == len(code_files))
            with open(code_pairs_file_path, 'wb') as f:
                pickle.dump(code_files, f)
            logger.info("Saving features into cached file %s", cache_file_path)
            torch.save(self.examples, cache_file_path)

        if 'train' in file_path:
            for idx, example in enumerate(self.examples[:3]):
                    logger.info("*** Example ***")
                    logger.info("idx: {}".format(idx))
                    logger.info("label: {}".format(example.label))
                    logger.info("input_tokens: {}".format([x.replace('\u0120','_') for x in example.input_tokens]))
                    logger.info("input_ids: {}".format(' '.join(map(str, example.input_ids))))



    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        
        return torch.tensor(self.examples[item].input_ids),torch.tensor(self.examples[item].label)


def load_and_cache_examples(args, tokenizer, evaluate=False,test=False,pool=None):
    # 问题是，我寻思你们也没cache啊....
    dataset = TextDataset(tokenizer, args, file_path=args.test_data_file if test else (args.eval_data_file if evaluate else args.train_data_file),block_size=args.block_size,pool=pool)
    return dataset

def set_seed(seed=42):
    random.seed(seed)
    os.environ['PYHTONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

def train(args, train_dataset, model, tokenizer,pool):
    """ Train the model """

    args.train_batch_size = args.per_gpu_train_batch_size * max(1, args.n_gpu)
    train_sampler = RandomSampler(train_dataset) if args.local_rank == -1 else DistributedSampler(train_dataset)
    
    train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=args.train_batch_size)
    args.max_steps=args.epoch*len( train_dataloader)
    args.save_steps=len( train_dataloader)
    args.warmup_steps=len( train_dataloader)
    args.logging_steps=len( train_dataloader)
    args.num_train_epochs=args.epoch
    # print('args.max_steps: ', args.max_steps)
    # print('args.warmup_steps: ', args.warmup_steps)

    model.to(args.device)
    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': args.weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=args.warmup_steps,
                                                num_training_steps=args.max_steps)
    if args.fp16:
        try:
            from apex import amp
        except ImportError:
            raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use fp16 training.")
        model, optimizer = amp.initialize(model, optimizer, opt_level=args.fp16_opt_level)

    # multi-gpu training (should be after apex fp16 initialization)
    if args.n_gpu > 1:
        model = torch.nn.DataParallel(model)

    # Distributed training (should be after apex fp16 initialization)
    if args.local_rank != -1:
        model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.local_rank],
                                                          output_device=args.local_rank,
                                                          find_unused_parameters=True)

    checkpoint_last = os.path.join(args.output_dir, 'checkpoint-last')
    scheduler_last = os.path.join(checkpoint_last, 'scheduler.pt')
    optimizer_last = os.path.join(checkpoint_last, 'optimizer.pt')
    if os.path.exists(scheduler_last):
        scheduler.load_state_dict(torch.load(scheduler_last))
    if os.path.exists(optimizer_last):
        optimizer.load_state_dict(torch.load(optimizer_last))
    # Train!
    logger.info("***** Running training *****")
    logger.info("  Num examples = %d", len(train_dataset))
    logger.info("  Num Epochs = %d", args.num_train_epochs)
    logger.info("  Instantaneous batch size per GPU = %d", args.per_gpu_train_batch_size)
    logger.info("  Total train batch size (w. parallel, distributed & accumulation) = %d",
                args.train_batch_size * args.gradient_accumulation_steps * (
                    torch.distributed.get_world_size() if args.local_rank != -1 else 1))
    logger.info("  Gradient Accumulation steps = %d", args.gradient_accumulation_steps)
    logger.info("  Total optimization steps = %d", args.max_steps)
    
    global_step = args.start_step
    tr_loss, logging_loss,avg_loss,tr_nb,tr_num,train_loss = 0.0, 0.0,0.0,0,0,0
    best_mrr=0.0
    best_f1=0
    # model.resize_token_embeddings(len(tokenizer))
    model.zero_grad()
    set_seed(args.seed)  # Added here for reproducibility (even between python 2 and 3)
 
    for idx in range(args.start_epoch, int(args.num_train_epochs)): 
        bar = tqdm(train_dataloader,total=len(train_dataloader))
        tr_num=0
        train_loss=0
        for step, batch in enumerate(bar):
            inputs = batch[0].to(args.device)        
            labels=batch[1].to(args.device) 
            model.train()
            loss,logits = model(inputs,labels)


            if args.n_gpu > 1:
                loss = loss.mean()  # mean() to average on multi-gpu parallel training
            if args.gradient_accumulation_steps > 1:
                loss = loss / args.gradient_accumulation_steps

            if args.fp16:
                with amp.scale_loss(loss, optimizer) as scaled_loss:
                    scaled_loss.backward()
                torch.nn.utils.clip_grad_norm_(amp.master_params(optimizer), args.max_grad_norm)
            else:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)

            tr_loss += loss.item()
            tr_num+=1
            train_loss+=loss.item()
            if avg_loss==0:
                avg_loss=tr_loss
            avg_loss=round(train_loss/tr_num,5)
            bar.set_description("epoch {} loss {}".format(idx,avg_loss))

                
            if (step + 1) % args.gradient_accumulation_steps == 0:
                optimizer.step()
                optimizer.zero_grad()
                scheduler.step()  
                global_step += 1
                output_flag=True
                avg_loss=round(np.exp((tr_loss - logging_loss) /(global_step- tr_nb)),4)
                if args.local_rank in [-1, 0] and args.logging_steps > 0 and global_step % args.logging_steps == 0:
                    logging_loss = tr_loss
                    tr_nb=global_step

                if args.local_rank in [-1, 0] and args.save_steps > 0 and global_step % args.save_steps == 0:
                    
                    if args.local_rank == -1 and args.evaluate_during_training:  # Only evaluate when single GPU otherwise metrics may not average well
                        results = evaluate(args, model, tokenizer,pool=pool,eval_when_training=True)                 
                        # Save model checkpoint

                    if results['eval_accuracy']>=best_f1:
                        best_f1=results['eval_accuracy']
                        logger.info("  "+"*"*20)  
                        logger.info("  Best acc:%s",round(best_f1,4))
                        logger.info("  "+"*"*20)                          
                        
                        checkpoint_prefix = 'checkpoint-best-f1'
                        output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))                        
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)                        
                        model_to_save = model.module if hasattr(model,'module') else model
                        ft = '_ft' if args.ft else ''
                        output_dir = os.path.join(output_dir, 'model_at{}.bin'.format(ft)) 
                        torch.save(model_to_save.state_dict(), output_dir)
                        logger.info("Saving model checkpoint to %s", output_dir)
                        
        if args.max_steps > 0 and global_step > args.max_steps:
            train_iterator.close()
            break
    return global_step, tr_loss / global_step


def evaluate(args, model, tokenizer, prefix="",pool=None,eval_when_training=False):
    # Loop to handle MNLI double evaluation (matched, mis-matched)
    eval_output_dir = args.output_dir
    eval_dataset = TextDataset(tokenizer, args,args.eval_data_file)
    # 得到数据集.
    if not os.path.exists(eval_output_dir) and args.local_rank in [-1, 0]:
        os.makedirs(eval_output_dir)

    args.eval_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)
    # Note that DistributedSampler samples randomly
    eval_sampler = SequentialSampler(eval_dataset) if args.local_rank == -1 else DistributedSampler(eval_dataset)
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=args.eval_batch_size,num_workers=4,pin_memory=True)

    # multi-gpu evaluate
    if args.n_gpu > 1 and eval_when_training is False:
        model = torch.nn.DataParallel(model)

    # Eval!
    logger.info("***** Running evaluation {} *****".format(prefix))
    logger.info("  Num examples = %d", len(eval_dataset))
    logger.info("  Batch size = %d", args.eval_batch_size)
    eval_loss = 0.0
    nb_eval_steps = 0
    model.eval()
    logits=[]  
    y_trues=[]
    for batch in tqdm(eval_dataloader):
        inputs = batch[0].to(args.device)        
        labels = batch[1].to(args.device) 
        with torch.no_grad():
            lm_loss,logit = model(inputs,labels)
            eval_loss += lm_loss.mean().item()
            logits.append(logit.cpu().numpy())
            y_trues.append(labels.cpu().numpy())
            # ground truth
        
        nb_eval_steps += 1
    logits=np.concatenate(logits,0)
    y_trues=np.concatenate(y_trues,0)
    best_threshold=0
    best_f1=0
    
    y_preds = []
    for logit in logits:
        y_preds.append(np.argmax(logit))
    print(y_trues)
    print(y_preds)
    from sklearn.metrics import recall_score
    recall=recall_score(y_trues, y_preds, average='macro')
    from sklearn.metrics import precision_score
    precision=precision_score(y_trues, y_preds, average='macro')   
    from sklearn.metrics import f1_score
    f1=f1_score(y_trues, y_preds, average='macro')
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_trues, y_preds)

    result = {
        "eval_recall": float(recall),
        "eval_precision": float(precision),
        "eval_f1": float(f1),
        "eval_accuracy": float(accuracy),
        "eval_threshold":best_threshold,
        
    }

    logger.info("***** Eval results {} *****".format(prefix))
    for key in sorted(result.keys()):
        logger.info("  %s = %s", key, str(round(result[key],4)))

    return result

def test(args, model, tokenizer, prefix="",pool=None,best_threshold=0):
    # Loop to handle MNLI double evaluation (matched, mis-matched)
    eval_dataset = load_and_cache_examples(args, tokenizer, test=True,pool=pool)

    args.eval_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)
    # Note that DistributedSampler samples randomly
    eval_sampler = SequentialSampler(eval_dataset) if args.local_rank == -1 else DistributedSampler(eval_dataset)
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=args.eval_batch_size,num_workers=4,pin_memory=True)

    # multi-gpu evaluate
    if args.n_gpu > 1:
        model = torch.nn.DataParallel(model)

    # Eval!
    logger.info("***** Running Test {} *****".format(prefix))
    logger.info("  Num examples = %d", len(eval_dataset))
    logger.info("  Batch size = %d", args.eval_batch_size)
    eval_loss = 0.0
    nb_eval_steps = 0
    model.eval()
    logits=[]  
    y_trues=[]
    for batch in tqdm(eval_dataloader):
        inputs = batch[0].to(args.device)        
        labels=batch[1].to(args.device) 
        with torch.no_grad():
            lm_loss,logit = model(inputs,labels)
            eval_loss += lm_loss.mean().item()
            logits.append(logit.cpu().numpy())
            y_trues.append(labels.cpu().numpy())
        nb_eval_steps += 1
    logits=np.concatenate(logits,0)
    y_preds=logits[:,1]>best_threshold
    with open(os.path.join(args.output_dir,"predictions.txt"),'w') as f:
        for example,pred in zip(eval_dataset.examples,y_preds):
            if pred:
                f.write(example.url1+'\t'+example.url2+'\t'+'1'+'\n')
            else:
                f.write(example.url1+'\t'+example.url2+'\t'+'0'+'\n')



def ASR(args, model, tokenizer):
    eval_dataset = TextDataset(tokenizer, args, file_path=args.eval_data_file)
    eval_sampler = SequentialSampler(eval_dataset)
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=1,num_workers=4)

    # adv_dataset = TextDataset(tokenizer, args, file_path=args.adv_data_file)
    # adv_sampler = SequentialSampler(adv_dataset)
    # adv_dataloader = DataLoader(adv_dataset, sampler=adv_sampler, batch_size=1,num_workers=4)
    # assert len(eval_dataloader) == len(adv_dataloader)

    #加载adv样本
    adv_codes = []
    with open(args.adv_data_file) as f:
        for line in f:
            adv_codes.append(line)
    print("adv codes num: ", len(adv_codes))
    assert(len(eval_dataloader) == len(adv_codes))

    logger.info("***** Attack Success Rate *****")
    logger.info("  Num examples = %d", len(adv_codes))
    model.eval()

    total_num = 0
    attack_success_num = 0
    for i, (example_eval) in enumerate(eval_dataloader):
        eval_inputs_id = example_eval[0].to(args.device) 
        eval_label = example_eval[1].to(args.device) 
        with torch.no_grad():
            eval_lm_loss, eval_logit = model(eval_inputs_id, eval_label)
            # eval_lm_loss, eval_logit = model(eval_inputs_id,eval_attn_mask,eval_position_idx,eval_label)

        eval_logit = eval_logit.cpu().numpy()
        eval_label = eval_label.cpu().numpy()[0]
        # print(np.argmax(eval_logit))
        # print(eval_label)
        # print(np.argmax(eval_logit) == eval_label)

        #样本原本分类正确则继续
        if np.argmax(eval_logit) == eval_label:
            total_num += 1
            adv_inputs_id = torch.tensor(convert_examples_to_features(adv_codes[i], eval_label, tokenizer, args).input_ids).unsqueeze(0).to(args.device)
            # print(eval_inputs_id.shape)
            # print(adv_inputs_id.shape)
            with torch.no_grad():
                adv_logit = model(adv_inputs_id)
            adv_logit = adv_logit.cpu().numpy()
            #对抗样本分类错误则攻击成功
            if np.argmax(adv_logit) != eval_label:
                attack_success_num += 1
            
    asr = attack_success_num / total_num
    result = {
        "ASR": asr,
        "total_num": total_num,
        "attack_success_num": attack_success_num
    }
    logger.info("***** Attack results *****")
    for key in sorted(result.keys()):
        logger.info("  %s = %s", key, str(round(result[key],4)))

    return result


def similarity(args, model, tokenizer):
    eval_dataset = TextDataset(tokenizer, args, file_path=args.eval_data_file)
    eval_sampler = SequentialSampler(eval_dataset)
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=1,num_workers=4)

    model.eval()

    list_similarity = []
    list_distance = []
    #pre-trained encoder
    if args.pretrained_encoder == 'codebert':
        model_sub = Model_sub(RobertaModel.from_pretrained("microsoft/codebert-base"), args).to(args.device)
    elif args.pretrained_encoder == 'graphcodebert':
        model_sub = gcb_Model_sub(RobertaForSequenceClassification.from_pretrained("microsoft/graphcodebert-base")).to(args.device)
    elif args.pretrained_encoder == 'codet5':
        try:
            model_sub = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-small").to(args.device)
        except:
            model_sub = T5ForConditionalGeneration.from_pretrained('../cache/Salesforce/codet5-small/').to(args.device)
        
    distance = nn.PairwiseDistance(p=2)
    for i, (example_eval) in enumerate(eval_dataloader):
        eval_inputs_id = example_eval[0].to(args.device) 
        eval_label = example_eval[1].to(args.device) 
        with torch.no_grad():
            eval_lm_loss, eval_logit, fine_tuned_embedding = model(eval_inputs_id, eval_label)
            # eval_lm_loss, eval_logit = model(eval_inputs_id,eval_attn_mask,eval_position_idx,eval_label)

        eval_logit = eval_logit.cpu().numpy()
        eval_label = eval_label.cpu().numpy()[0]
        # print(np.argmax(eval_logit))
        # print(eval_label)
        # print(np.argmax(eval_logit) == eval_label)

        #样本原本分类正确则继续
        if np.argmax(eval_logit) == eval_label:            
            #pre-trained embedding
            pre_trained_embedding = model_sub(eval_inputs_id) #torch.Size([1, 510, 768])
            # print('pre_trained_embedding.shape: ', pre_trained_embedding.shape)
            similarity = torch.cosine_similarity(torch.flatten(pre_trained_embedding[0]), torch.flatten(fine_tuned_embedding[0]), dim=0)
            # print('similarity.shape: ', similarity.shape)
            list_similarity.append(similarity.item())
            list_distance.append(distance(torch.flatten(pre_trained_embedding[0]), torch.flatten(fine_tuned_embedding[0])).item())

    print('feature_similarity: ', np.mean(list_similarity))
    print('feature_distance: ', np.mean(list_distance))
    print(len(list_similarity))

    return 

                                                
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
    parser.add_argument("--adv_data_file", default=None, type=str,
                        help="An optional input evaluation data file to evaluate the perplexity on (a text file).")
    parser.add_argument("--pretrained_encoder", default=None, type=str,
                        help="An optional input evaluation data file to evaluate the perplexity on (a text file).")
                    
    parser.add_argument("--model_type", default="bert", type=str,
                        help="The model architecture to be fine-tuned.")
    parser.add_argument("--model_name_or_path", default=None, type=str,
                        help="The model checkpoint for weights initialization.")
    parser.add_argument("--number_labels", type=int,
                        help="The model checkpoint for weights initialization.")

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
    parser.add_argument("--do_asr", action='store_true',
                        help="Whether to run asr on the dev set.")
    parser.add_argument("--do_sim", action='store_true',
                        help="Whether to run asr on the dev set.")
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
    parser.add_argument('--ft', action='store_true',
                        help="fine-tune the classifer only")
    parser.add_argument('--fp16', action='store_true',
                        help="Whether to use 16-bit (mixed) precision (through NVIDIA apex) instead of 32-bit")
    parser.add_argument('--fp16_opt_level', type=str, default='O1',
                        help="For fp16: Apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']."
                             "See details at https://nvidia.github.io/apex/amp.html")
    parser.add_argument("--local_rank", type=int, default=-1,
                        help="For distributed training: local_rank")
    parser.add_argument('--server_ip', type=str, default='', help="For distant debugging.")
    parser.add_argument('--server_port', type=str, default='', help="For distant debugging.")

    
    pool = multiprocessing.Pool(cpu_cont)
    args = parser.parse_args()

    # Setup distant debugging if needed
    if args.server_ip and args.server_port:
        # Distant debugging - see https://code.visualstudio.com/docs/python/debugging#_attach-to-a-local-script
        import ptvsd
        print("Waiting for debugger attach")
        ptvsd.enable_attach(address=(args.server_ip, args.server_port), redirect_output=True)
        ptvsd.wait_for_attach()

    # Setup CUDA, GPU & distributed training
    if args.local_rank == -1 or args.no_cuda:
        device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
        args.n_gpu = torch.cuda.device_count()
    else:  # Initializes the distributed backend which will take care of sychronizing nodes/GPUs
        torch.cuda.set_device(args.local_rank)
        device = torch.device("cuda", args.local_rank)
        torch.distributed.init_process_group(backend='nccl')
        args.n_gpu = 1
    args.device = device
    args.per_gpu_train_batch_size=args.train_batch_size//args.n_gpu
    args.per_gpu_eval_batch_size=args.eval_batch_size//args.n_gpu
    # Setup logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO if args.local_rank in [-1, 0] else logging.WARN)
    logger.warning("Process rank: %s, device: %s, n_gpu: %s, distributed training: %s, 16-bits training: %s",
                   args.local_rank, device, args.n_gpu, bool(args.local_rank != -1), args.fp16)

    # Set seed
    set_seed(args.seed)

    # Load pretrained model and tokenizer
    if args.local_rank not in [-1, 0]:
        torch.distributed.barrier()  # Barrier to make sure only the first process in distributed training download model & vocab

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
    config.num_labels=args.number_labels
    tokenizer = tokenizer_class.from_pretrained(args.tokenizer_name,
                                                do_lower_case=args.do_lower_case,
                                                cache_dir=args.cache_dir if args.cache_dir else None)
    if args.block_size <= 0:
        args.block_size = tokenizer.max_len_single_sentence  # Our input block size will be the max possible for the model
    args.block_size = min(args.block_size, tokenizer.max_len_single_sentence)
    if args.model_name_or_path:
        encoder = model_class.from_pretrained(args.model_name_or_path,
                                            from_tf=bool('.ckpt' in args.model_name_or_path),
                                            config=config,
                                            cache_dir=args.cache_dir if args.cache_dir else None)    
    else:
        encoder = model_class(config)

    model = Model(encoder,config,tokenizer,args)
    model_for_sim=Model_for_sim(encoder,config,tokenizer,args)
    if args.ft:
        print('Freezing the encoder...')
        model.freeze_encoder()
    # load 模型.
    if args.local_rank == 0:
        torch.distributed.barrier()  # End of barrier to make sure only the first process in distributed training download model & vocab

    logger.info("Training/evaluation parameters %s", args)

    # Training
    if args.do_train:
        if args.local_rank not in [-1, 0]:
            torch.distributed.barrier()  # Barrier to make sure only the first process in distributed training process the dataset, and the others will use the cache

        train_dataset = TextDataset(tokenizer, args,args.train_data_file)

        if args.local_rank == 0:
            torch.distributed.barrier()

        #------------------------------------------------------------
        checkpoint_prefix = 'checkpoint-best-f1/model.bin'
        output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
        model.load_state_dict(torch.load(output_dir))
        #------------------------------------------------------------

        global_step, tr_loss = train(args, train_dataset, model, tokenizer,pool)


    # Evaluation
    results = {}
    if args.do_eval and args.local_rank in [-1, 0]:
        ft = '_ft' if args.ft else ''
        checkpoint_prefix = 'checkpoint-best-f1/model{}.bin'.format(ft)
        output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
        model.load_state_dict(torch.load(output_dir))
        model.to(args.device)
        result=evaluate(args, model, tokenizer,pool=pool)
        
    if args.do_test and args.local_rank in [-1, 0]:
        ft = '_ft' if args.ft else ''
        checkpoint_prefix = 'checkpoint-best-f1/model.bin'
        output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
        model.load_state_dict(torch.load(output_dir))
        model.to(args.device)
        test(args, model, tokenizer,pool=pool,best_threshold=0.5)

    if args.do_asr and args.local_rank in [-1, 0]:
        checkpoint_prefix = 'checkpoint-best-f1/model.bin'
        output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))    
        model.load_state_dict(torch.load(output_dir))         
        model.to(args.device)
        result=ASR(args, model, tokenizer)
        logger.info("***** Attack results *****")
        for key in sorted(result.keys()):
            logger.info("  %s = %s", key, str(round(result[key],4)))

    if args.do_sim and args.local_rank in [-1, 0]:
        checkpoint_prefix = 'checkpoint-best-f1/model.bin'
        output_dir = os.path.join(args.output_dir, '{}'.format(checkpoint_prefix))  
        model_for_sim.load_state_dict(torch.load(output_dir))
        model_for_sim.to(args.device)
        similarity(args, model_for_sim, tokenizer)

    return results


if __name__ == "__main__":
    main()