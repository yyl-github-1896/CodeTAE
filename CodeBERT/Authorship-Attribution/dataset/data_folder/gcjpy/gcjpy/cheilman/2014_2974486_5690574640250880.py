#!/usr/bin/python
 
 import sys
 
 import puzutils
 
 class Minesweeper_2014_QC(puzutils.CodeJamProblem):
   def __init__(self, inputFilename):
     puzutils.CodeJamProblem.__init__(self, inputFilename)
 
     self.T = None
 
   def load(self):
     """
       input:
 
       T (number of test cases)
 
       R C M (integers)
 
     """
 
     self.tests = []
 
     with open(self.inputFilename, "rt") as file:
       self.T = int(file.readline().strip())
 
       for i in xrange(self.T):
         (R,C,M) = [int(x) for x in file.readline().split(' ')]
 
         self.tests.append([R,C,M])
 
     return True
 
   def boardToString(self, board):
     retval = ""
 
     for row in board:
       retval = retval + "\n" + "".join(row)
 
     return retval
 
   def executeTest(self, test):
     """
       Run a test and return output.
     """
 
     (R,C,M) = test
     #print "R: %d, C: %d, M: %d" % (R,C,M)
 
     spaces = R * C
     blanks = spaces - M
 
     if (blanks <= 0):
       #print "R: %d, C: %d, M: %d, spaces: %d, blanks: %d" % (R,C,M,spaces,blanks)
       return "Impossible"
 
     board = [['.' for x in range(C)] for y in range(R)]
 
     board[R-1][C-1] = "c"
 
     badpositions=[]
     positions=[]
 
     for x in xrange(C):
       for y in xrange(R):
         if (x == (C-1)) and (y == (R-1)):
           continue
         if (x == (C-1)) and (y == (R-2)):
           badpositions.append((x,y))
           continue
         if (x == (C-2)) and (y == (R-1)):
           badpositions.append((x,y))
           continue
         if (x == (C-2)) and (y == (R-2)):
           badpositions.append((x,y))
           continue
 
         positions.append((x,y))
 
     positions.reverse()
 
     for x in badpositions:
       positions.insert(0, x)
 
     m = M
 
     while (m > 0):
       if len(positions) <= 0:
         #return self.boardToString(board)
         return "Impossible"
 
       pos = positions.pop()
       (x,y) = pos
 
       if (board[y][x] != "."):
         #return self.boardToString(board)
         return "Impossible"
 
       board[y][x] = '*'
       m = m - 1
 
     mines = sum([x.count('*') for x in board])
 
     if (mines != M):
       #return self.boardToString(board)
       return "Impossible"
 
     if (blanks > 1):
       if (R > 1):
         if board[R - 2][C - 1] == "*":
           #return self.boardToString(board)
           return "Impossible"
 
       if (C > 1):
         if board[R - 1][C - 2] == "*":
           #return self.boardToString(board)
           return "Impossible"
 
       if (R > 1) and (C > 1):
         if board[R - 2][C - 2] == "*":
           #return self.boardToString(board)
           return "Impossible"
 
     #return "Possible"
     return self.boardToString(board)
 
 with Minesweeper_2014_QC(sys.argv[1]) as problem:
   problem.load()
 
   problem.run()
