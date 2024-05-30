import sys
 
 def pointsWar(naomi, ken, N):
 	points = 0
 	iNaomi = 0
 	iKen = 0
 	while iNaomi < N and iKen < N:
 		if naomi[iNaomi] > ken[iKen]:
 			points += 1
 		else:
 			iNaomi += 1
 		iKen += 1
 	return points
 
 def pointsDeceitfulWar(naomi, ken, N):
 	points = N
 	iNaomi = 0
 	iKen = 0
 	while iNaomi < N and iKen < N:
 		if naomi[iNaomi] > ken[iKen]:
 			iKen += 1
 		else:
 			points -= 1
 		iNaomi += 1
 	return points
 
 ##########################################################
 # Main
 
 inputFileName = sys.argv[1]
 
 f = file(inputFileName)
 fout = file("output.txt", "w")
 
 T = int(f.readline())
 
 for case in xrange(T):
 	N = int(f.readline().strip())
 	naomi = f.readline().strip().split()
 	ken = f.readline().strip().split()
 
 	for i in xrange(N):
 		naomi[i] = (float(naomi[i]),"N")
 		ken[i] = (float(ken[i]),"K")
 
 	naomi.sort()
 	ken.sort()
 
 	##### Output writing
 	fout.write("Case #%d: %d %d\n" %(case + 1, pointsDeceitfulWar(naomi, ken, N), pointsWar(naomi, ken, N)))
