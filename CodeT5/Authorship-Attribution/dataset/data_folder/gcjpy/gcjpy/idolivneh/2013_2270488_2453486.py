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
 	
 ############################################################
 #### add solution here 									####
 #### don't forget to change data from str to int/float  ####
 ############################################################
 
 def check_row(row):
 	if row.count('X') == 4:
 		return 'X'
 	if row.count('O') == 4:
 		return 'O'
 	if row.count('X') == 3 and row.count('T') == 1:
 		return 'X'
 	if row.count('O') == 3 and row.count('T') == 1:
 		return 'O'
 	if row.count('.') > 0:
 		return '.'
 	return 'F'
 		
 
 def calc_result(case):
 	case = case[:-1]
 	print "\t%s" % case
 	
 	rows = []
 	for row in case:
 		#print "\trow: '%s'" % row[0]
 		rows.append(row[0])
 	
 	for i in xrange(4):
 		column = ""
 		for j in xrange(4):
 			column += case[j][0][i]
 		#print "\trow: '%s'" % column
 		rows.append(column)
 	
 	diag1 = ""
 	diag2 = ""
 	for i in xrange(4):
 		diag1 += case[i][0][i]
 		diag2 += case[3-i][0][i]
 	#print "\trow: '%s'" % diag1
 	#print "\trow: '%s'" % diag2
 	rows.append(diag1)
 	rows.append(diag2)
 	
 	res = []
 	for row in rows:
 		res.append(check_row(row))
 	
 	if res.count('X'):
 		if res.count('O'):
 			raise IOError('both X and O won')
 		else:
 			result = "X won"
 	else:
 		if res.count('O'):
 			result = "O won"
 		else:
 			if res.count('.'):
 				result = "Game has not completed"
 			else:
 				result = "Draw"
 	
 	print "\t%s" % res
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
 		for case_index, case in iterate_cases_nlpc(filepath, 5):
 			
 			print "case #%d: time:%.02f" % (case_index, time.time() - start_time)
 			result = calc_result(case)
 			
 			#######################
 			#### format output ####
 			#######################
 			f_out.write("Case #%d: %s\n" % (case_index, result))
 				
 if __name__ == '__main__':
 	main(sys.argv[1])
