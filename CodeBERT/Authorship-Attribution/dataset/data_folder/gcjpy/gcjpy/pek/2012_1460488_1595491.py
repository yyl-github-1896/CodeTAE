from sys import stdin
 
 T = int(stdin.readline())
 for i in xrange(1,T+1):
 	ns = map(int, stdin.readline().split())
 	N,S,p = ns[0:3]
 	
 	h = 0
 	z = 0
 
 	for n in ns[3:]:
 		if n <= 1:
 			if n >= p: h += 1	
 		elif (n+2) // 3 >= p:
 			h += 1
 		elif (n+4) // 3 >= p:
 			z += 1
 
 	print "Case #%d: %d" % (i, h + min(S,z))
 
 
