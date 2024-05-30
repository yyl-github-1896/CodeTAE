#!/usr/bin/env python
 import sys
 
 
 def process(chosen_row_1, arrange_1, chosen_row_2, arrange_2):
 	rlt = 'Volunteer cheated!'
 	found = False
 	for i in arrange_1[chosen_row_1]:
 		if i in arrange_2[chosen_row_2]:
 			if not found:
 				rlt = i
 				found = True
 			else:
 				rlt = 'Bad magician!'
 				break
 	return rlt
 
 input_file = open(sys.argv[1], 'r')
 T = int(input_file.readline())
 for i in range(T):
 	chosen_row_1 = int(input_file.readline()) - 1
 	arrange_1 = []
 	arrange_1.append(map(int, input_file.readline().split()))
 	arrange_1.append(map(int, input_file.readline().split()))
 	arrange_1.append(map(int, input_file.readline().split()))
 	arrange_1.append(map(int, input_file.readline().split()))
 	chosen_row_2 = int(input_file.readline()) - 1
 	arrange_2 = []
 	arrange_2.append(map(int, input_file.readline().split()))
 	arrange_2.append(map(int, input_file.readline().split()))
 	arrange_2.append(map(int, input_file.readline().split()))
 	arrange_2.append(map(int, input_file.readline().split()))
 	print 'Case #%d:' % (i + 1), process(chosen_row_1, arrange_1, chosen_row_2, arrange_2)
