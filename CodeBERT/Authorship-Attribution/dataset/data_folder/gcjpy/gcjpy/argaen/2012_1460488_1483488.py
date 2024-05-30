t = int(raw_input())
 
 def mover(n, i):
 	s = str(n)
 	return int(s[i:] + s[:i])
 
 for i in range(t):
 	s = raw_input().split(' ')
 	a = int(s[0])
 	b = int(s[1])
 	total = 0
 	for n in range(a, b):
 		ms = []
 		for k in range(len(s[0])):
 			m = mover(n, k+1)
 			if m <= b and m > n and not m in ms:
 			#	print n, mover(n, k+1), k+1
 				ms.append(m)
 				total +=1
 
 
 	print 'Case #'+str(i+1)+':', total