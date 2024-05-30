import sys	
 
 inputFileName = sys.argv[1]
 
 f = file(inputFileName)
 fout = file("output.txt", "w")
 
 T = eval(f.readline())
 
 for case in xrange(T):
 
 	####First question
 	A1 = int(f.readline().strip())
 
 	for i in xrange(4):
 		if i == A1 - 1:
 			possibles1 = f.readline().strip().split(" ")
 		else:
 			f.readline().strip().split(" ")
 
 	####Second question
 	A2 = int(f.readline().strip())
 
 	for i in xrange(4):
 		if i == A2 - 1:
 			possibles2 = f.readline().strip().split(" ")
 		else:
 			f.readline().strip().split(" ")
 
 	final = []
 	for item in possibles2:
 		if item in possibles1:
 			final.append(item)
 
 	##### Output writing
 	if len(final) == 0:	
 		fout.write("Case #%d: Volunteer cheated!\n" %(case + 1))
 	elif len(final) == 1:
 		fout.write("Case #%d: %s\n" %(case + 1, final[0]))
 	else:
 		fout.write("Case #%d: Bad magician!\n" %(case + 1))
