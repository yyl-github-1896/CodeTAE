import sys
 
 def cycle_shift(in_str):
 	return "%s%s" % (in_str[-1], in_str[:-1])
 
 def get_cyclic_shifts(num):
 	results = []
 	str_num = str(num)
 	for _ in xrange(len(str_num) - 1):
 		str_num = cycle_shift(str_num)
 		if str_num[0] == '0':
 			continue
 		number = int(str_num)
 		if not number in results:
 			results.append(number)
 	return results
 	
 def get_rec_pairs(A, B):
 	rec_pairs = []
 	for i in xrange(A, B + 1):
 		shifts = get_cyclic_shifts(i)
 		for shift in shifts:
 			if (shift > i and
 				shift <= B):
 				rec_pairs.append((i, shift))
 	return rec_pairs
 	
 def main(filepath):
 	with file('numbers_output.txt', 'wb') as f_out:
 		with file(filepath, 'rb') as f_in:
 			for line_index, line in enumerate(f_in):
 				if line_index == 0: #T
 					continue
 				input_list = line.strip().split(' ')
 				A = int(input_list[0])
 				B = int(input_list[1])
 				
 				rec_pairs = get_rec_pairs(A, B)
 				result = len(rec_pairs)
 							
 				print
 				print line.strip()
 				print result
 				
 				f_out.write("Case #%d: %d\n" % (line_index, result))
 				
 if __name__ == '__main__':
 	main(sys.argv[1])