from array import array
 
 def Lawnmower(infile="B-small-attempt0.in", outfile="B-small-attempt0.out"):
 	inF = open(infile, 'r')
 	outF = open(outfile, 'w')
 	
 	for t in range(1, int(inF.readline().strip()) + 1):
 		#read grid size
 		temp = inF.readline().strip().split()
 		N = int(temp[0])
 		M = int(temp[1])
 		L = []
 		
 		for i in range(N):
 			L.append(inF.readline().strip().split()) #using an array should speed up the lookups
 			for j in range(M):
 				L[i][j] = int(L[i][j])
 		
 		for y in range(N):
 			for x in range(M):
 				# check horizontal
 				for i in range(M):
 					if L[y][i] > L[y][x]:
 						break
 				else:
 					continue
 				
 				# check vertical
 				for i in range(N):
 					if L[i][x] > L[y][x]:
 						break
 				else:
 					continue
 				break
 			else:
 				continue
 			break
 		else:
 			#good
 			outF.write("Case #" + str(t) + ": YES\n")
 			continue
 		#bad
 		outF.write("Case #" + str(t) + ": NO\n")
 	
 	#closing files
 	inF.close()
 	outF.close()
 	
 	#so I dont need to cat the file after
 	f = open(outfile, 'r')
 	print f.read()
 	f.close()
 	
 	
 if __name__ == "__main__":
     Lawnmower()