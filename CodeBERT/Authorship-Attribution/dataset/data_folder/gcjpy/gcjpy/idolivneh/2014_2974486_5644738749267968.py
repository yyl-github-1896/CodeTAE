import sys
 import time
 import itertools #use combinations!
 import random
 
 def iterate_cases_1lpc(filepath):	#1lpc = 1 line per case
 	with file(filepath, 'rb') as f_in:
 		for line_index, line in enumerate(f_in):
 			if line_index == 0: #T
 				continue
 			yield line_index, line.strip().split(' ')
 
 def iterate_cases_nlpc(filepath, n):	#1lpc = n line per case
 	with file(filepath, 'rb') as f_in:
 		case_counter = 1
 		case = []
 		for line_index, line in enumerate(f_in):
 			if line_index == 0: #T
 				continue
 			case.append(line.strip().split(' '))
 			if not line_index % n:
 				yield case_counter, case
 				case_counter += 1
 				case = []
 
 def iterate_cases_glpc(filepath):		#glpc - given lines per case
 	with file(filepath, 'rb') as f_in:
 		case_counter = 0
 		new_case = True
 		for line_index, line in enumerate(f_in):
 			if line_index == 0: #T
 				continue
 			if new_case:
 				new_case = False
 				case_counter += 1
 				case = []
 				assert len(line.strip().split(' ')) == 1
 				lines_left = int(line.strip())
 				if not lines_left:
 					new_case = True
 					yield case_counter, case
 				continue
 			if lines_left:
 				lines_left -= 1
 				case.append(line.strip().split(' '))
 			if not lines_left:
 				new_case = True
 				yield case_counter, case
 			
 def part_of_list_to_int(array, flags):
 	assert len(array) == len(flags)
 	output = []
 	for index, elem in enumerate(array):
 		if flags[index]:
 			output.append(int(elem))
 		else:
 			output.append(elem)
 	return output
 
 def list_to_int(array):
 	return part_of_list_to_int(array, [True] * len(array))
 
 def part_of_list_to_float(array, flags):
 	assert len(array) == len(flags)
 	output = []
 	for index, elem in enumerate(array):
 		if flags[index]:
 			output.append(float(elem))
 		else:
 			output.append(elem)
 	return output
 
 def list_to_float(array):
 	return part_of_list_to_float(array, [True] * len(array))
 
 def get_max_array_on_index(array, index):
 	elem_len = len(array[0])
 	assert index < elem_len
 	for elem in array:
 		assert elem_len == len(elem)
 	max_sub = array[0][index]
 	max_elem = array[0]
 	for elem in array:
 		if elem[index] > max_sub:
 			max_sub = elem[index]
 			max_elem = elem
 	return max_elem
 
 def list_index_in_sorted_with_position(a_list, value, pos):
 	list_len = len(a_list)
 	if list_len == 1:
 		if a_list[0] == value:
 			return pos
 		return -1
 	if a_list[list_len/2] > value:
 		return list_index_in_sorted_with_position(a_list[:(list_len/2)], value, pos)
 	else:
 		return list_index_in_sorted_with_position(a_list[(list_len/2):], value, pos + (list_len/2))
 	
 def list_index_in_sorted_list(a_list, value):
 	return list_index_in_sorted_with_position(a_list, value, 0)
 
 def copy_list(list):
 	res = []
 	for elem in list:
 		res.append(elem)
 	return res	
 
 ############################################################
 #### add solution here 									####
 #### don't forget to change data from str to int/float  ####
 ############################################################
 
 def war_answer_simulator(blocks, choice):
 	over_arr = []
 	for elem in blocks:
 		if elem > choice:
 			over_arr.append(elem)
 	if not over_arr:
 		return min(blocks)
 	return min(over_arr)
 
 def war_counter(a, b):
 	count = 0
 	while len(a) and len(b):
 		if a[0] > b[0]:
 			count += 1
 		else:
 			b.pop(0)
 		a.pop(0)
 	return count
 
 def dec_counter(a, b):
 	count = 0
 	while len(a) and len(b):
 		if a[0] < b[0]:
 			pass
 		else:
 			b.pop(0)
 			count += 1
 		a.pop(0)
 	return count	
 	
 def solve(N, N_blocks, K_blocks):
 	res = None
 	
 	N_blocks.sort()
 	K_blocks.sort()
 	N_blocks_copy = copy_list(N_blocks)
 	K_blocks_copy = copy_list(K_blocks)
 	
 	N_blocks_copy.reverse()
 	K_blocks_copy.reverse()
 	
 	war_count = war_counter(N_blocks_copy, K_blocks_copy)
 	print 'war', war_count
 	
 	dec_count = dec_counter(N_blocks, K_blocks)
 	print 'dec', dec_count
 	
 	return '%d %d' % (dec_count, war_count)
 	
 	
 def calc_result(case):
 	result = None
 	
 	N = int(case[0][0])
 	N_blocks = list_to_float(case[1])
 	K_blocks = list_to_float(case[2])
 	print N
 	print N_blocks
 	print K_blocks
 	
 	result = solve(N, N_blocks, K_blocks)
 	print result
 	
 	return result
 
 def main(filepath):
 	start_time = time.time()
 	with file('output.txt', 'wb') as f_out:
 		
 		######################################
 		#### select input iteration type: ####
 		####	- iterate_cases_1lpc	  ####
 		####	- iterate_cases_nlpc +n	  ####
 		####	- iterate_cases_glpc	  ####
 		######################################
 		for case_index, case in iterate_cases_nlpc(filepath, 3):
 			
 			print "case #%d: time:%.02f" % (case_index, time.time() - start_time)
 			result = calc_result(case)
 			
 			#######################
 			#### format output ####
 			#######################
 			f_out.write("Case #%d: %s\n" % (case_index, result))
 				
 if __name__ == '__main__':
 	main(sys.argv[1])
