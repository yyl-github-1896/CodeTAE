#!/usr/bin/env python
 
 import fileinput
 
 def checkIndex(index,num,numB):
 	n=int(str(num)[index:]+str(num)[:index])
 	if n > num and n <= numB:
 		#print "pair",num, n
 		return n
 	else: return False
 
 
 for line in fileinput.input():
 	if fileinput.isfirstline():
 		T=int(line) # no. of test cases
 		continue
 	numStrs=line.split()
 	numSize=len(numStrs[0])
 	numA=int(numStrs[0])
 	numB=int(numStrs[1])
 	count=0
 	for num in xrange(numA, numB+1):
 		pairs=set()
 		for i in range(numSize):
 			n=checkIndex(i,num, numB)
 			if n:
 				pairs.add(n)
 		count +=len(pairs)
 				
 	print "Case #%(k)i: %(count)i" % {"k":fileinput.lineno()-1,"count":count}
 	