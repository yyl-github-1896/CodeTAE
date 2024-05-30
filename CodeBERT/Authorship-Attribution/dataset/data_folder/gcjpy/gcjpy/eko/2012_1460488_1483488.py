import sys, os
 import re
 
 tCase = int(sys.stdin.readline())
 
 def alien(numbers):
 	resul = 0
 	A = int(numbers[0])
 	B = int(numbers[1])
 
 	for n in range(A,B-1):
 		for m in range(n+1,B+1):
 			#print n,m
 			if (len(str(n)) == len(str(m))):
 				resul += isRecycled(str(n),str(m))
 	
 
 
 	return resul
 	
 def isRecycled(n,m):
 	if len(n) < 2:
 		return 0
 		
 	for c in m:
 		if c not in n:
 			return 0
 
 	for i in range (1, len(n)):
 		mi = m[i:] + m[-len(m):-(len(m)-i)]
 		if n == mi:
 			return 1
 	
 	return 0
 
 
 lines = []
 for i in xrange(tCase):
 	line = sys.stdin.readline().split()
 	lines.append((line[0],line[1]))
 	
 
 for i in xrange(tCase):	
 	#case.append(frase)
 	print "Case #%d: %s" % (i+1, alien(lines[i]))
 	
 	
 
