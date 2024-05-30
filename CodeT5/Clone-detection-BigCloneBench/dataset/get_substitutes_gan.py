import os
import pickle
import json
import sys
import copy
import random
import torch
import torch.nn as nn
import argparse
from tqdm import tqdm


sys.path.append('../../../')
sys.path.append('../../../python_parser')

from python_parser.run_parser import get_identifiers, remove_comments_and_docstrings
from transformers import (RobertaModel, RobertaForMaskedLM, RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer)
from transformers import (T5Config, T5ForConditionalGeneration,)
from utils import is_valid_variable_name, _tokenize, get_identifier_posistions_from_code, get_masked_code_by_position, get_substitutes, is_valid_substitute, _tokenize


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



class GeneticAlgorithm():

    def __init__(self, initial_population):
        '''
        initial_population: the initial population for the genetic algorithm
        '''
        self.device = torch.device('cuda:0')
        self.initial_population = initial_population
        self.model_sub = T5ForConditionalGeneration.from_pretrained('../cache/Salesforce/codet5-small/').to(self.device)
        self.tokenizer = RobertaTokenizer.from_pretrained('../cache/Salesforce/codet5-small')
        try:
            self.tokenizer_mlm = RobertaTokenizer.from_pretrained("Salesforce/codet5-small")
        except:
            self.tokenizer_mlm = RobertaTokenizer.from_pretrained("../cache/Salesforce/codet5-small")
        self.targeted = False
        self.args = args
        # alphabate for all the possible variable names: 大写字母，小写字母，数字，下划线
        self.alphabate = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)] + ['_'] + ['$']
        self.iter_nums = 5   # number of genetic algorithm iterations/generations
        self.child_nums = len(self.initial_population)  # how many childern are born in each generation
        self.mutation_prob = 0.5   # the probability that a new chromesome is generated through mutation
        self.population_size = 20   # must be an even number
    

    # def convert_code_to_features(self, code):
    #     code_tokens = self.tokenizer.tokenize(code)[:self.args.block_size-2]
    #     source_tokens = [self.tokenizer.cls_token]+code_tokens+[self.tokenizer.sep_token]
    #     source_ids = self.tokenizer.convert_tokens_to_ids(source_tokens)
    #     padding_length = self.args.block_size - len(source_ids)
    #     source_ids += [self.tokenizer.pad_token_id]*padding_length
    #     return InputFeatures(source_tokens,source_ids, 0)

    def convert_code_to_embedding(self, code):
        input_ids = self.tokenizer(code, return_tensors="pt").input_ids.to(self.device)
        attention_mask = input_ids.ne(self.tokenizer.pad_token_id).to(self.device)
        outputs = self.model_sub(input_ids=input_ids, attention_mask=attention_mask,
                               labels=input_ids, decoder_attention_mask=attention_mask, output_hidden_states=True)['decoder_hidden_states'][-1].sum(dim=1).squeeze()
        return outputs


    def loss(self, embedding_a, embedding_b):
        '''
        compute the squared distance between embedding_a and embedding_b
        '''        
        return nn.MSELoss()(embedding_a.to('cuda'), embedding_b.to('cuda')).item()
    

    def compute_fitness(self, embedding_target, chromesome):
        '''
        compute the fitness of the chromesome
        '''    
        if len(chromesome) == 0:
            return -1e10
        processed_code_chromesome = " ".join(chromesome)
        embedding_chromesome = self.convert_code_to_embedding(processed_code_chromesome)
        
        feature_distance = self.loss(embedding_target, embedding_chromesome)
        return feature_distance
    

    def mutate(self, chromesome, mutation_type=None):
        '''
        four kinds of mutation operation: insert, delete, flip, swap
        '''
        is_variable = False
        iteration_num = 0
        if len(chromesome) == 0:
            return chromesome
        while not is_variable:
            if mutation_type not in range(4):
                mutation_type = random.choice(range(4))
            if mutation_type == 0: # insert
                insert_position = random.choice(range(len(chromesome) + 1))
                insert_char = random.choice(self.alphabate)
                new_chromesome = chromesome[:insert_position] + insert_char + chromesome[insert_position:]
            elif mutation_type == 1: # delete
                delete_position = random.choice(range(len(chromesome)))
                new_chromesome = chromesome[:delete_position] + chromesome[delete_position + 1:]
            elif mutation_type == 2: # flip
                flip_position = random.choice(range(len(chromesome)))
                flip_char = random.choice(self.alphabate)
                new_chromesome = chromesome[:flip_position] + flip_char + chromesome[flip_position+1:]
            elif mutation_type == 3: # swap
                if len(chromesome) == 1:
                    new_chromesome = chromesome
                else:
                    pos_1, pos_2 = random.sample(range(len(chromesome)), 2)
                    if pos_1 > pos_2:  # pos_1 must be samller than pos_2
                        temp_pos = pos_1
                        pos_1 = pos_2
                        pos_2 = temp_pos
                    temp_char_1 = chromesome[pos_1]
                    temp_char_2 = chromesome[pos_2]
                    # print('pos_1: {}, pos_2: {}, temp_char_1: {}, temp_char_2: {}'.format(pos_1, pos_2, temp_char_1, temp_char_2))  # for debugging
                    new_chromesome = chromesome[:pos_1] + temp_char_2 + chromesome[pos_1+1:pos_2] + temp_char_1 + chromesome[pos_2+1:]
            else:
                raise Exception('mutation_type out of range!')
            is_variable = is_valid_variable_name(new_chromesome, lang='java')
            if new_chromesome in self.initial_population:
                is_variable = False
            iteration_num += 1
            if iteration_num > 10:
                break

        return 
    
    def crossover(self, chromesome_a, chromesome_b, cross_position=None):
        is_variable = False
        iteration_num = 0
        if min(len(chromesome_a), len(chromesome_b)) <= 1:
            return chromesome_a, chromesome_b
        while not is_variable:
            child_a, child_b = '', ''
            # 随机选择交叉位置，但是不能选到0
            cross_position = random.choice(range(1, min(len(chromesome_a), len(chromesome_b))))

            child_a += chromesome_a[:cross_position]
            child_a += chromesome_b[cross_position:]

            child_b += chromesome_a[cross_position:]
            child_b += chromesome_b[:cross_position]
            is_variable = is_valid_variable_name(child_a, lang='java') and is_valid_variable_name(child_b, lang='java')
            iteration_num += 1
            if iteration_num > 10:
                break
        return child_a, child_b


    def get_substitutes(self, tgt_variable):
        '''
        tgt_variable: a variable in the source code to be replaced
        '''
        processed_code_target = tgt_variable
        embedding_target = self.convert_code_to_embedding(processed_code_target)

        # scale down the initial population
        population = list(self.initial_population)
        fitness_values = []
        for chromesome in population:
            fitness_values.append(self.compute_fitness(embedding_target, chromesome))
        avg_fitness = sum(fitness_values) / len(fitness_values)
        print('initial population, average fitness: {}'.format(avg_fitness))
        assert len(fitness_values) == len(population)
        sorted_population = [i for _, i in sorted(zip(fitness_values, population), reverse=True)]
        population = sorted_population[:self.population_size]

        for its in range(self.iter_nums):
            new_population = []
            if random.uniform(0, 1) < self.mutation_prob:
                for chromesome in population:
                    new_population.append(self.mutate(chromesome))
            else:
                random.shuffle(population)
                num_parents = int(len(population) / 2)
                for parent_id in range(num_parents):
                    chromesome_a = population[parent_id]
                    chromesome_b = population[num_parents + parent_id]
                    child_a, child_b = self.crossover(chromesome_a, chromesome_b)
                    new_population += [child_a, child_b]
            new_population = [elem for elem in new_population if elem is not None]
            new_fitness_values = []
            for chromesome in new_population:
                new_fitness_values.append(self.compute_fitness(embedding_target, chromesome))
            population = population + new_population
            fitness_values = fitness_values + new_fitness_values

            # delete all the repeated chromosome
            pop_2_values = {}
            for i in range(len(population)):
                pop_2_values[population[i]] = fitness_values[i]
            population = list(pop_2_values.keys())
            fitness_values = list(pop_2_values.values())

            sorted_population = [key for _, key in sorted(zip(fitness_values, population), reverse=True)]
            sorted_values = [value for value, _ in sorted(zip(fitness_values, population), reverse=True)]
            population = sorted_population[:self.population_size]
            fitness_values = sorted_values[:self.population_size]

        avg_fitness = sum(fitness_values) / len(fitness_values)

        return population




def main():


    eval_data = []

    tokenizer_mlm = RobertaTokenizer.from_pretrained("../cache/Salesforce/codet5-small")

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

    # collect all the variable names as the initial population
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
                if ' ' in name[0].strip() or name[0] is None:
                    continue
                all_substitutes_set.add(name[0])
        print('all the variable names in the dataset have been collected! Total number: {}'.format(len(all_substitutes_set)))


    with open(args.store_path, "w") as wf:
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


            ga_generator = GeneticAlgorithm(initial_population=all_substitutes_set)
            variable_substitute_dict = {}
            for tgt_word in variable_names:
                generated_substitutes = ga_generator.get_substitutes(tgt_variable=tgt_word)
                for tmp_substitute in all_substitutes_set:
                    if tmp_substitute.strip() in variable_names:
                        continue
                    if not is_valid_substitute(tmp_substitute.strip(), tgt_word, 'java'):
                        continue
                    try:
                        variable_substitute_dict[tgt_word].append(tmp_substitute)
                    except:
                        variable_substitute_dict[tgt_word] = [tmp_substitute]
            item["substitutes"] = variable_substitute_dict
            wf.write(json.dumps(item)+'\n')

    print('file saved at {}!'.format(args.store_path))
            

if __name__ == "__main__":
    main()


# nohup bash scripts_subs.sh >get_substitutes_gan.log 2>&1 &