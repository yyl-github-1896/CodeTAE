import sys
 
 def testLine(i, lawn):
 	return (2 not in lawn[i])
 
 def testColumn(j, lawn):
 	possible = True
 	for line in lawn:
 		if line[j] == 2:
 			possible = False
 			break
 	return possible
 
 ##########################################################
 # Main
 
 inputFileName = sys.argv[1]
 
 f = file(inputFileName)
 fout = file("output.txt", "w")
 
 T = eval(f.readline())
 
 for case in xrange(T):
 	data = f.readline().split()
 	N = eval(data[0])
 	M = eval(data[1])
 	possible = True
 	if N == 1 or M == 1:
 		for i in xrange(N):
 			f.readline()
 	else:
 		lawn = []
 		for i in xrange(N):
 			line = f.readline().strip().split()
 			for j in xrange(M):
 				line[j] = eval(line[j])
 			lawn.append(line)
 		i = 0
 		while i < N and possible:
 			for j in xrange(M):
 				if lawn[i][j] == 1:
 					if not testLine(i, lawn):
 						if not testColumn(j, lawn):
 							possible = False
 			i += 1
 
 	##### Output writing
 	fout.write("Case #%d: " %(case + 1))
 	if possible:
 		fout.write("YES\n")
 	else:
 		fout.write("NO\n")
