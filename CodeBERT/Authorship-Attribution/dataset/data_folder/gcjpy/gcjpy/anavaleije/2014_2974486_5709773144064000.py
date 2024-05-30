import sys
 
 def oneMoreFarm(C, F, nFarms):
 	return C/(2.0 + nFarms*F)
 	
 
 ##########################################################
 # Main
 
 inputFileName = sys.argv[1]
 
 f = file(inputFileName)
 fout = file("output.txt", "w")
 
 T = int(f.readline().strip())
 
 for case in xrange(T):
 
 	data = f.readline().split()
 	C = eval(data[0])
 	F = eval(data[1])
 	X = eval(data[2])
 
 	tmin = X/2.0
 	foundMin = False
 
 	S = 0
 	nFarms = 0
 
 	while not foundMin:
 		nFarms += 1
 		S += oneMoreFarm(C, F, nFarms - 1)
 		t = S + X/(2.0 + nFarms*F)
 		if t < tmin:
 			tmin = t
 		else:
 			foundMin = True
 
 	##### Output writing
 	fout.write("Case #%d: %.7f\n" %(case + 1, tmin))
