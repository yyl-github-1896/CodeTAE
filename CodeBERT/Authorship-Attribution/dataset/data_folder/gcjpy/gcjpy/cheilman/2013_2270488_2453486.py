#!/usr/bin/python
 
 import sys
 
 def readfile(file):
   """
     input:
 
 		T (number of test cases)
 
 		xxxx
 		xxxx
 		xxxx
 		xxxx	(T boards, where x in [X,O,T,.]
 
   """
 
   tests = []
 
   T = int(file.readline().strip())
 
   for i in xrange(T):
 		board = ""
     
 		for j in xrange(4):
 			line = file.readline().strip()
 
 			board = board + line
 
 		file.readline()
 
 		tests.append(board)
 
   return tests
 
 def fourInARow(who, test):
 	"""
 		Find four of 'who' in a row (T wild).
 	"""
 
 	target = (who, 'T')
 
 	# Horizontal/Vertical
 	for i in range(4):
 		horzWin = True
 		vertWin = True
 
 		for j in range(4):
 			horzIndex = i * 4 + j
 			vertIndex = j * 4 + i
 
 			if not (test[horzIndex] in target):
 				horzWin = False
 
 			if not (test[vertIndex] in target):
 				vertWin = False
 
 		if horzWin or vertWin:
 			return True
 
 	# Diagonal
 	slashWin = True
 	bslashWin = True
 
 	for i in range(4):
 		x = y = i
 
 		slashIndex = y * 4 + x
 		bslashIndex = y * 4 + (3 - x)
 
 		#print "Checking (%d,%d) = %s and (%d,%d) = %s" % (x, y, test[slashIndex], 3-x, y, test[bslashIndex])
 
 		if not (test[slashIndex] in target):
 			slashWin = False
 
 		if not (test[bslashIndex] in target):
 			bslashWin = False
 
 	if slashWin or bslashWin:
 		return True
 
 	return False
 
 def run(test):
 	"""
 		Run a test and return output.
 	"""
 
 	if fourInARow('X', test):
 		return "X won"
 	elif fourInARow('O', test):
 		return "O won"
 	elif '.' in test:
 		return "Game has not completed"
 	else:
 		return "Draw"
 
 file = open(sys.argv[1], "rt")
 
 tests = readfile(file)
 
 file.close()
 
 case = 1
 
 for test in tests:
 #if True:
   #test = tests[0]
   result = run(test)
   print "Case #%d: %s" % (case, result)
   case = case + 1
