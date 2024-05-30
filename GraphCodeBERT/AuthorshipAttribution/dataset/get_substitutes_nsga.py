import os
import pickle
import json
import sys
import copy
import random
import torch
import torch.nn as nn
import argparse

sys.path.append('../../../')
sys.path.append('../../../python_parser')

# from attacker import 
from python_parser.run_parser import get_identifiers, remove_comments_and_docstrings, python_keywords
from transformers import (RobertaForMaskedLM, RobertaConfig, RobertaModel, RobertaForSequenceClassification, RobertaTokenizer)
from tqdm import tqdm
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

    def __init__(self, initial_population,):
        '''
        initial_population: the initial population for the genetic algorithm
        '''
        self.initial_population = initial_population
        self.model_sub = RobertaModel.from_pretrained(args.base_model).to('cuda')
        self.tokenizer = RobertaTokenizer.from_pretrained(args.base_model)
        self.tokenizer_mlm = RobertaTokenizer.from_pretrained(args.base_model)
        
        self.targeted = False
        self.args = args
        # alphabate for all the possible variable names: 大写字母，小写字母，数字，下划线
        self.alphabate = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)] + ['_']
        self.iter_nums = 10   # number of genetic algorithm iterations/generations
        self.child_nums = len(self.initial_population)  # how many childern are born in each generation
        self.mutation_prob = 0.5   # the probability that a new chromesome is generated through mutation
        self.population_size = 60   # must be an even number
        

    def convert_code_to_features(self, code):
        code_tokens = self.tokenizer.tokenize(code)[:self.args.block_size-2]
        source_tokens = [self.tokenizer.cls_token]+code_tokens+[self.tokenizer.sep_token]
        source_ids = self.tokenizer.convert_tokens_to_ids(source_tokens)
        padding_length = self.args.block_size - len(source_ids)
        source_ids += [self.tokenizer.pad_token_id]*padding_length
        return InputFeatures(source_tokens,source_ids, 0)


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
            return -1e10, -100
        processed_code_chromesome = " ".join(chromesome)
        input_ids_chromesome = self.convert_code_to_features(processed_code_chromesome).input_ids
        embedding_chromesome = self.model_sub(torch.tensor(input_ids_chromesome).unsqueeze(0).to('cuda'))[0].detach().cpu()
        
        feature_distance = self.loss(embedding_target, embedding_chromesome)
        return feature_distance, -len(chromesome)

    def sort(self, population, fitness_values_1, fitness_values_2):
        sorted_population = []
        sorted_fitness_values_1 = []
        sorted_fitness_values_2 = []
        max_fitness_with_index_1 = max(((num, index) for index, num in enumerate(fitness_values_1)), key=lambda x: x[1])
        max_index_1 = max_fitness_with_index_1[1]
        sorted_population.append(population[max_index_1])
        sorted_fitness_values_1.append(fitness_values_1[max_index_1])
        sorted_fitness_values_2.append(fitness_values_2[max_index_1])
        population.pop(max_index_1)
        fitness_values_1.pop(max_index_1)
        fitness_values_2.pop(max_index_1)
        
        max_fitness_with_index_2 = max(((num, index) for index, num in enumerate(fitness_values_2)), key=lambda x: x[1])
        max_index_2 = max_fitness_with_index_2[1]
        sorted_population.append(population[max_index_2])
        sorted_fitness_values_1.append(fitness_values_1[max_index_2])
        sorted_fitness_values_2.append(fitness_values_2[max_index_2])
        population.pop(max_index_2)
        fitness_values_1.pop(max_index_2)
        fitness_values_2.pop(max_index_2)

        return sorted_population, sorted_fitness_values_1, sorted_fitness_values_2


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
            is_variable = is_valid_variable_name(new_chromesome, lang='python')
            if new_chromesome in self.initial_population:
                is_variable = False
            iteration_num += 1
            if iteration_num > 10:
                break

        return new_chromesome

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
            is_variable = is_valid_variable_name(child_a, lang='python') and is_valid_variable_name(child_b, lang='python')
            iteration_num += 1
            if iteration_num > 10:
                break
        return child_a, child_b


    def get_substitutes(self, tgt_variable):
        '''
        tgt_variable: a variable in the source code to be replaced
        '''
        processed_code_target = tgt_variable
        input_ids_target = self.convert_code_to_features(processed_code_target).input_ids
        embedding_target = self.model_sub(torch.tensor(input_ids_target).unsqueeze(0).to('cuda'))[0].detach().cpu()

        # scale down the initial population
        population = list(self.initial_population)
        fitness_values_1 = []
        fitness_values_2 = []
        for chromesome in population:
            ft_1, ft_2 = self.compute_fitness(embedding_target, chromesome)
            fitness_values_1.append(ft_1)
            fitness_values_2.append(ft_2)
        avg_fitness_1 = sum(fitness_values_1) / len(fitness_values_1)
        avg_fitness_2 = sum(fitness_values_2) / len(fitness_values_2)
        print('initial population, average fitness 1: {}, fitness 2: {}'.format(avg_fitness_1, avg_fitness_2))
        assert len(fitness_values_1) == len(fitness_values_2) == len(population)

        sorted_population, sorted_fitness_values_1, sorted_fitness_values_2 = self.sort(population, fitness_values_1, fitness_values_2)
        population = sorted_population[:self.population_size]
        fitness_values_1 = sorted_fitness_values_1[:self.population_size]
        fitness_values_2 = sorted_fitness_values_2[:self.population_size]

        for its in range(self.iter_nums):
            new_population = []
            if random.uniform(0, 1) < self.mutation_prob:
                # do mutation for the whole population
                # print('iteration {}, doing mutation...'.format(its))
                for chromesome in population:
                    new_population.append(self.mutate(chromesome))
            else:
                # do crossover for the whole population
                # print('iteration {}, doing crossover...'.format(its))
                random.shuffle(population)
                num_parents = int(len(population) / 2)
                for parent_id in range(num_parents):
                    chromesome_a = population[parent_id]
                    chromesome_b = population[num_parents + parent_id]
                    child_a, child_b = self.crossover(chromesome_a, chromesome_b)
                    new_population += [child_a, child_b]
            new_fitness_values_1 = []
            new_fitness_values_2 = []
            for chromesome in new_population:
                results = self.compute_fitness(embedding_target, chromesome)
                ft_1, ft_2 = self.compute_fitness(embedding_target, chromesome)
                new_fitness_values_1.append(ft_1)
                new_fitness_values_2.append(ft_2)
            population = population + new_population
            fitness_values_1 = fitness_values_1 + new_fitness_values_1
            fitness_values_2 = fitness_values_2 + new_fitness_values_2

            # delete all the repeated chromosome
            pop_2_values_1 = {}
            pop_2_values_2 = {}
            for i in range(len(population)):
                pop_2_values_1[population[i]] = (fitness_values_1[i])
                pop_2_values_2[population[i]] = (fitness_values_2[i])
            population = list(pop_2_values_1.keys())
            fitness_values_1 = list(pop_2_values_1.values())
            fitness_values_2 = list(pop_2_values_2.values())

        avg_fitness_1 = sum(fitness_values_1) / len(fitness_values_1)
        avg_fitness_2 = sum(fitness_values_2) / len(fitness_values_2)
        print('after GA, average fitness_1: {}, fitness_2: {}'.format(avg_fitness_1, avg_fitness_2))
        print('population[:5]: {}, population[-5:]: {}'.format(population[:5], population[-5:]))


        # # Unit Test for mutation
        # chromesome = population[0]
        # new_chromesome = self.mutate(chromesome, mutation_type=3)
        # print('original chromesome: {}, new chromesome: {}'.format(chromesome, new_chromesome))

        # # Unit Test for crossover
        # chromesome_a, chromesome_b = population[0], population[1]
        # child_a, child_b = self.crossover(chromesome_a, chromesome_b)
        # print('chromesome before crossover: {}, {}. after: {}, {}'.format(chromesome_a, chromesome_b, child_a, child_b))

        return population



def main():

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


    # collect all the variable names as the initial population
    with open(args.store_path, "w") as wf:
        all_substitutes_set = set()

        for item in tqdm(eval_data):
            try:
                identifiers, code_tokens = get_identifiers(remove_comments_and_docstrings(item["code"], "python"), "python")
            except:
                identifiers, code_tokens = get_identifiers(item["code"], "python")
            processed_code = " ".join(code_tokens)
            
            words, sub_words, keys = _tokenize(processed_code, tokenizer_mlm)

            for name in identifiers:
                if ' ' in name[0].strip():
                    continue
                all_substitutes_set.add(name[0])
        print('all the variable names in the dataset have been collected! Total number: {}'.format(len(all_substitutes_set)))


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
            
            ga_generator = GeneticAlgorithm(initial_population=all_substitutes_set)
            variable_substitute_dict = {}
            for tgt_word in variable_names:
                generated_substitutes = ga_generator.get_substitutes(tgt_variable=tgt_word)
                for tmp_substitute in generated_substitutes:
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

            
    print('file saved at {}!'.format(args.store_path))
            

if __name__ == "__main__":
    main()
