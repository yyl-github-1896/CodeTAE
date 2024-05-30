def find_recycled(n, b):
 	ns = str(n)
 	reclist = []
 	for i in xrange(1, len(ns), 1):
 		nrec = ns[i:len(ns)] + ns[0:i]
 		if nrec[0] != "0":
 			nrec = eval(nrec)
 			if nrec <= b and nrec > n and (n, nrec) not in reclist:
 				reclist.append((n,nrec))
 	return len(reclist)
 
 inp = file("input.in")
 T = eval(inp.readline())
 out = file("output.txt", "w")
 
 for i in xrange(T):
 	a, b = inp.readline().strip().split()
 	a = eval(a)
 	b = eval(b)
 	nrec = 0
 	reclist = []
 	for n in xrange(a, b):
 		if n > 11:
 			nrec += find_recycled(n, b)
 	out.write("Case #%d: %d\n" %(i + 1, nrec))
 			
