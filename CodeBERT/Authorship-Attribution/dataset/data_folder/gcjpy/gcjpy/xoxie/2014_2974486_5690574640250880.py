import sys
 from collections import deque
 
 def makeBoardR(b):
 	numR, numC, numMines, filledR, filledC = b
 	q = numMines / numR
 	r = numMines % numR
 
 	if q <= numC-2 and r == 0:
 		board = ["*"*(filledC + numC) for x in range (filledR)]
 		board.append( "*"*(filledC+q)+"."*(numC-q) )
 		board.append( "*"*(filledC+q)+"."*(numC-q-1)+"c" )
 		output = "\n".join(board)
 	elif numMines == numR * numC - 1:
 		board = ["*"*(filledC + numC) for x in range (filledR+1)]
 		board.append( "*"*(filledC+numC-1)+"c" )
 		output = "\n".join(board)
 	else:
 		output = "Impossible"
 
 	return output
 
 def makeBoardC(b):
 	numR, numC, numMines, filledR, filledC = b
 	q = numMines / numC
 	r = numMines % numC
 
 	if q <= numR-2 and r == 0:
 		board = ["*"*(filledC+numC) for x in range(filledR+q)]
 		for x in range( numR-1-q ):
 			board.append( "*"*filledC + ".." )
 		board.append( "*"*filledC + ".c" )
 		output = "\n".join(board)
 	elif numMines == numR * numC - 1:
 		board = ["*"*(filledC+numC) for x in range(filledR+numR-1)]
 		board.append( "*"*(filledC+numC-1) + "c" )
 		output = "\n".join(board)
 	else:
 		output = "Impossible"
 	return output
 
 def makeBoard(b):
 	numR, numC, numMines, filledR, filledC = b
 	q = numMines / (numC-2)
 	r = numMines % (numC-2)
 
 	board = ["*"*(numC+filledC) for x in range(filledR)]
 	for x in range(q):
 		board.append( "*"*(numC-2+filledC)+".." )
 	board.append( "*"*(r+filledC)+"."*(numC-r) )
 	for x in range(numR-q-2):
 		board.append( "*"*filledC+"."*numC )
 	board.append( "*"*filledC + "."*(numC-1) + "c" )
 	return "\n".join(board)
 
 def makeBoard0(b):
 	numR,numC,numMines,filledR,filledC = b
 	board = ["*"*(numC+filledC) for x in range(filledR)]
 	for x in range(numR-1):
 		board.append( "*"*(filledC)+"."*numC )
 	board.append( "*"*(filledC) + "."*(numC-1) + "c" )
 	return "\n".join(board)
 
 f = open( sys.argv[1] )
 f.readline()
 
 numCase = 1
 l = f.readline()
 while l != "":
 	numR, numC, numMines = [int(x) for x in l.split()]
 
 	boards = deque()
 	if numR == 1:
 		if numC == 1 and numMines == 0:
 			output = "c"
 		elif numC == 1 and numMines > 0:
 			output = "Impossible"
 		else:
 			output = "*"*numMines + "."*(numC-numMines-1) + "c"
 	elif numC == 1:
 		output = "\n".join("*"*numMines + "."*(numR-numMines-1) + "c")
 	else:
 		boards.append( (numR,numC,numMines,0,0) )
 		output = "Impossible"
 
 	while output == "Impossible" and len(boards) > 0:
 		b = boards.popleft()
 		#print b
 		numR,numC,numMines,filledR,filledC = b
 		if numMines == 0:
 			output = makeBoard0(b)
 			break
 
 		if numMines >= numC and numR > 2:
 			boards.append( (numR-1,numC,numMines-numC,filledR+1,filledC) )
 		if numMines >= numR and numC > 2:
 			boards.append( (numR,numC-1,numMines-numR,filledR,filledC+1) )
 
 		if numMines <= (numR-2)*(numC-2):
 			output = makeBoard(b)
 
 		if numR == 2:
 			output = makeBoardR(b)
 
 		if numC == 2:
 			output = makeBoardC(b)
 		
 	print "Case #"+str(numCase)+":\n"+output
 	#print "Case #"+str(numCase)+": " +l+output
 	l = f.readline()
 	numCase += 1
