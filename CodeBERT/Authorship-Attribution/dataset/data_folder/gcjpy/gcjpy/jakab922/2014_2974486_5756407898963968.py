T = int(raw_input().strip())
 
 for j in xrange(T):
 	row_num1 = int(raw_input().strip())
 	for i in xrange(4):
 		if i + 1 == row_num1:
 			row1 = set(map(int, raw_input().strip().split(' ')))
 		else:
 			raw_input()
 	row_num2 = int(raw_input().strip())
 	for i in xrange(4):
 		if i + 1 == row_num2:
 			row2 = set(map(int, raw_input().strip().split(' ')))
 		else:
 			raw_input()
 	common = row1 & row2
 	lc = len(common)
 	if lc == 1:
 		stuff = list(common)[0]
 	elif lc > 1:
 		stuff = "Bad magician!"
 	else:
 		stuff = "Volunteer cheated!"
 
 	print "Case #%s: %s" % (j + 1, stuff)
