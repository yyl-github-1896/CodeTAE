import sys, os
 import re
 
 tCase = int(sys.stdin.readline())
 
 def alien(frases,case):
 	
 	case = case.replace('(','[')
 	case = case.replace(')',']')
 	#print frases,case
 	
 	ER1 = re.compile(case, re.I)
 	count = 0
 	for frase in frases:
 		#print ER1.search(frase)
 		if ER1.search(frase):
 			count += 1
 	return count
 
 
 for i in xrange(tCase):	
 	linha = sys.stdin.readline().split()
 	#S = linha[0]
 	P = int(linha[1])
 	T = int(linha[2])
 	list = []
 	for j in range (3,len(linha)):
 		list.append(int(linha[j]))
 	list.sort(reverse=True)
 	#print S,P,T,list
 	realT = T*3 - 2
 	supT = realT - 2
 	
 	count = 0
 	for item in list:
 		if item >= realT:
 			count += 1
 		elif P > 0 and item >= supT and T >= 2:
 			count += 1
 			P -= 1
 		elif P > 0 and item >= realT and T == 1:
 			count += 1
 			P -= 1
 		elif T == 0:
 			count += 1
 		else:
 			break
 		
 	#case.append(frase)
 	print "Case #%d: %d" % (i+1, count)
 	
 	
 
