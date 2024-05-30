#!/usr/bin/python3
 
 import sys
 import math
 
 def findbest(score):
 	# Corner case
 	if score == 0: return (0, 0)
 
 	best = math.ceil(score / 3)
 	bestsurp = round(score / 3) + 1
 
 	return (best, bestsurp)
 	
 # Ignore the number of cases
 sys.stdin.readline()
 
 casenum = 0
 for line in sys.stdin:
 	casenum += 1
 
 	data = line.strip().split(' ')
 	maxsurprising = int(data[1])
 	p = int(data[2])
 	scores = data[3:]
 	maxgooglers = 0
 
 	for s in scores:
 		(best, bestsurp) = findbest(int(s))
 		if best >= p:
 			maxgooglers += 1
 		else:
 			if bestsurp >= p and maxsurprising > 0:
 				maxgooglers += 1
 				maxsurprising -= 1
 
 	print("Case #%d: %d" % (casenum, maxgooglers))
