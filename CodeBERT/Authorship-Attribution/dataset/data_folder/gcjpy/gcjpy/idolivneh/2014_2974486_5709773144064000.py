import sys
 import time
 import itertools #use combinations!
 
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
 
 def solve(C, F, X):
 	farms_num = 0
 	waiting_for_farms = 0
 	production_rate = 2
 	final_run_time = X / production_rate
 	result = final_run_time + waiting_for_farms
 	
 	print "%d: prod_rate:%.02f, final_run:%.02f, farm_wait:%.02f, tot:%.06f" % (farms_num,
 																				production_rate,
 																				final_run_time,
 																				waiting_for_farms,
 																				result)
 		
 
 	
 	while True:
 		farms_num += 1
 		waiting_for_farms += C / production_rate
 		production_rate += F
 		final_run_time = X / production_rate
 		new_result = final_run_time + waiting_for_farms
 		print "%d: prod_rate:%.02f, final_run:%.02f, farm_wait:%.02f, tot:%.06f" % (farms_num,
 																					production_rate,
 																					final_run_time,
 																					waiting_for_farms,
 																					new_result)
 		if new_result > result:
 			return result
 		result = new_result
 	
 def calc_result(case):
 	result = None
 	
 	C = float(case[0])
 	F = float(case[1])
 	X = float(case[2])
 	print C, F, X
 	
 	result = solve(C, F, X)
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
 		for case_index, case in iterate_cases_1lpc(filepath):
 			
 			print "case #%d: time:%.02f" % (case_index, time.time() - start_time)
 			result = calc_result(case)
 			
 			#######################
 			#### format output ####
 			#######################
 			f_out.write("Case #%d: %.07f\n" % (case_index, result))
 				
 if __name__ == '__main__':
 	main(sys.argv[1])
