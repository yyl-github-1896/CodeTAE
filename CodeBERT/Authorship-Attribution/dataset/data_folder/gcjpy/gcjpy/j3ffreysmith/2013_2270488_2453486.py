def checkRow(r):
 	c = r[0];
 	
 	# making sure it isnt an empty line
 	if (c == '.'):
 		return (False, None)
 		
 	for i in range(1,4):
 		if not (r[i] == c or r[i] == 'T'):
 			return (False, None)
 	
 	# if it got this far it must be right
 	return (True, c)
 
 def checkCol(L, col):
 	c = L[0][col];
 	
 	# making sure it isnt an empty line
 	if (c == '.'):
 		return (False, None)
 		
 	for i in range(1,4):
 		if not (L[i][col] == c or L[i][col] == 'T'):
 			return (False, None)
 	
 	# if it got this far it must be right
 	return (True, c)
 	
 def checkDiag(L):
 	c = L[0][0];
 	
 	for i in range(1,4):
 		if not (L[i][i] == c or L[i][i] == 'T'):
 			break
 	else:
 		if (c != '.'):
 			# if it got this far it must be right
 			return (True, c)
 	
 	#first diag failed
 	c = L[0][3];
 	
 	# making sure it isnt an empty line
 	if (c == '.'):
 		return (False, None)
 		
 	for i in range(1,4):
 		if not (L[i][3-i] == c or L[i][3-i] == 'T'):
 			break
 	else:
 		# if it got this far it must be right
 		return (True, c)
 		
 	return (False, None)
 		
 def checkComplete(L):
 	for i in range(4):
 		if '.' in L[i]:
 			return False
 	return True
 
 def TicTacToeTomek(infile="A-small-attempt0.in", outfile="A-small-attempt0.out"):
 	f = open(infile, 'r')
 	out = open(outfile, 'w')
 	
 	# get the number of tests
 	n = int(f.readline().strip())
 	
 	for t in range(1, n + 1):
 		L = []
 		# loading game
 		for i in range(4):
 			L.append(f.readline().strip());
 		
 		# checking game state
 		for i in range(4):
 			#checking row
 			result = checkRow(L[i])
 			if result[0]:
 				out.write("Case #" + str(t) + ": " + result[1] + " won\n")
 				break
 			#checking column
 			result = checkCol(L,i)
 			if result[0]:
 				out.write("Case #" + str(t) + ": " + result[1] + " won\n")
 				break
 		else:
 			#checking column
 			result = checkDiag(L)
 			if result[0]:
 				out.write("Case #" + str(t) + ": " + result[1] + " won\n")
 			else:
 				if checkComplete(L):
 					out.write("Case #" + str(t) + ": Draw\n")
 				else:
 					out.write("Case #" + str(t) + ": Game has not completed\n")
 				
 		f.readline() #skipping empty line
 	
 	#closing files
 	f.close()
 	out.close()
 	
 	#so I dont need to cat the file after
 	f = open(outfile, 'r')
 	print f.read()
 	f.close()
 	
 	
 if __name__ == "__main__":
     TicTacToeTomek()