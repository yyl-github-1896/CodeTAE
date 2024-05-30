import sys
 
 def testSymbol(symbol, game):
 	if testLines(symbol, game):
 		return True
 	elif testColumns(symbol, game):
 		return True
 	elif testDiagonals(symbol, game):
 		return True
 	else:
 		return False
 
 def testLines(symbol, game):
 	i = 0
 	won = False
 	while (i < 4 and not won):
 		line = game[i]
 		c = line.count(symbol)
 		if c == 4 or (c == 3 and "T" in line):
 			won = True
 		i += 1
 	return won
 
 def transpose(game):
 	for i in xrange(3):
 		for j in xrange(i + 1, 4):
 			aux = game[i][j]
 			game[i][j] = game[j][i]
 			game[j][i] = aux
 	return game
 
 def testColumns(symbol, game):
 	game = transpose(game)
 	return testLines(symbol, game)
 
 def testDiagonals(symbol, game):
 	won1 = True
 	won2 = True
 	i = 0
 	while i < 4 and (won1 or won2):
 		if game[i][i] not in [symbol, "T"]:
 			won1 = False
 		if game[i][3 - i] not in [symbol, "T"]:
 			won2 = False
 		i += 1
 	return (won1 or won2)		
 
 inputFileName = sys.argv[1]
 
 f = file(inputFileName)
 fout = file("output.txt", "w")
 
 T = eval(f.readline())
 
 for i in xrange(T):
 	game = []
 	for j in xrange(4):
 		line = f.readline().strip()
 		gameLine = 4*[None]
 		for k in xrange(4):
 			gameLine[k] = line[k]
 		game.append(gameLine)
 	f.readline()
 	if testSymbol("X", game):
 		gameResult = "X"
 	elif testSymbol("O", game):
 		gameResult = "O"
 	elif "." not in game[0] and "." not in game[1] and "." not in game[2] and "." not in game[3]:
 		gameResult = "Draw\n"
 	else:
 		gameResult = "Game has not completed\n"
 
 	fout.write("Case #%d: " %(i + 1))
 	if gameResult in ["X", "O"]:
 		fout.write("%s won\n" %(gameResult))
 	else:
 		fout.write(gameResult)
