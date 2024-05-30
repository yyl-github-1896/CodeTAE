#!/usr/bin/python3
 
 import sys
 
 def findrecycled(num, A, B):
 	strnum = str(num)
 	results = {}
 	for i in range(1, len(strnum)):
 		strrecycled = strnum[i:] + strnum[0:i]
 		recycled = int(strrecycled)
 		if recycled > num and recycled >= A and recycled <= B:
 			results["%d_%d" % (num, recycled)] = 1
 	return len(results)
 
 # Ignore the number of cases
 sys.stdin.readline()
 
 casenum = 0
 for line in sys.stdin:
 	casenum += 1
 
 	data = line.strip().split(' ')
 	A = int(data[0])
 	B = int(data[1])
 
 	count = 0
 	for num in range(A, B):
 		count += findrecycled(num, A, B)
 
 	print("Case #%d: %d" % (casenum, count))
