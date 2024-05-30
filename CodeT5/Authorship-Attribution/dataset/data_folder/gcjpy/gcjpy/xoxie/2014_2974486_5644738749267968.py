import sys
 from collections import deque
 
 f = open(sys.argv[1])
 f.readline()
 
 numCase = 1
 l = f.readline()
 while l != "":
 	n = [float(x) for x in f.readline().split()]
 	k = [float(x) for x in f.readline().split()]
 
 	n.sort()
 	nd = deque(n)
 	k.sort()
 	kd = deque(k)
 
 	war = 0
 	while len(nd) > 0:
 		nblock = nd.pop()
 		if nblock > kd[-1]:
 			kd.popleft()
 			war += 1
 		else:
 			kd.pop()
 
 	all = [ (x,1) for x in n ]
 	all.extend( [(x,2) for x in k] )
 	all.sort()
 
 	dwar = 0
 	nd = deque(n)
 	kd = deque(k)
 	while len(nd) > 0:
 		if nd[0] < kd[0]:
 			kd.pop()
 		else:
 			kd.popleft()
 			dwar += 1
 		nd.popleft()
 		
 	print "Case #"+str(numCase)+ ": "+str(dwar)+" "+str(war)
 	
 
 	numCase += 1
 	l = f.readline()