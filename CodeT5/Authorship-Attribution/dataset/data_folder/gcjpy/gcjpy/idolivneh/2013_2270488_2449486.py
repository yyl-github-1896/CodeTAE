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
 				assert len(line.strip().split(' ')) == 2
 				N = int(line.strip().split(' ')[0])
 				M = int(line.strip().split(' ')[1])
 				lines_left = N
 				case.append(N)
 				case.append(M)
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
 	
 ############################################################
 #### add solution here 									####
 #### don't forget to change data from str to int/float  ####
 ############################################################
 def test_row(row, value):
 	for elem in row:
 		if elem > value:
 			return False
 	return True
 
 def calc_result(case):
 	#print "\t%s" % case[2:]
 	N = case[0]
 	M = case[1]
 	rows = []
 	for str_row in case[2:]:
 		rows.append(list_to_int(str_row))
 	#print "\trows: %s" % rows
 	columns = []
 	for i in xrange(M):
 		column = []
 		for j in xrange(N):
 			column.append(rows[j][i])
 		columns.append(column)
 	#print "\tcolumns: %s" % columns
 	
 	for i in xrange(N):
 		for j in xrange(M):
 			if not (test_row(rows[i], rows[i][j]) or test_row(columns[j], rows[i][j])):
 				print "i,j: %d,%d" % (i, j)
 				result = "NO"
 				print "\t%s" % result
 				return result
 	
 	result = "YES"
 	print "\t%s" % result
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
 		for case_index, case in iterate_cases_glpc(filepath):
 			
 			print "case #%d: time:%.02f" % (case_index, time.time() - start_time)
 			result = calc_result(case)
 			
 			#######################
 			#### format output ####
 			#######################
 			f_out.write("Case #%d: %s\n" % (case_index, result))
 				
 if __name__ == '__main__':
 	main(sys.argv[1])
