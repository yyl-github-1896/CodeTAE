import sys
 
 n = int(sys.stdin.readline())
 for i in range(n):
 	inputline = sys.stdin.readline().strip()
 	inputparams = inputline.split()
 
 	a = int(inputparams[0])
 	b = int(inputparams[1])
 
 	k = a
 	ndigits = 0
 	while k > 0:
 		k /= 10
 		ndigits += 1
 
 	cnt = 0
 
 	dic = {}
 
 	for n1digits in range(1, ndigits / 2 + 1):
 		n2digits = ndigits - n1digits
 
 		for n1 in range(a / (10 ** n2digits), b / (10 ** n2digits) + 1):
 			for n2 in range(a / (10 ** n1digits), b / (10 ** n1digits) + 1):
 
 				k1 = n1 * 10 ** n2digits + n2
 				k2 = n2 * 10 ** n1digits + n1
 
 				if (n1digits == n2digits) and (n1 >= n2):
 					continue
 
 				if (k1 != k2) and (k1 >=a) and (k2 >= a) and (k1 <= b) and (k2 <= b):
 
 					if min(k1, k2) not in dic:
 						dic[min(k1, k2)] = set()
 
 					if max(k1, k2) not in dic[min(k1, k2)]:
 						dic[min(k1, k2)].add(max(k1, k2))
 						cnt += 1
 
 	print "Case #%d: %d" % (i + 1, cnt)	
 
