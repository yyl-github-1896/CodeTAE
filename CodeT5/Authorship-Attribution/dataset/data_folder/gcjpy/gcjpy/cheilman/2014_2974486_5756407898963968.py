#!/usr/bin/python
 
 import sys
 
 import puzutils
 
 class Magic_2014_QA(puzutils.CodeJamProblem):
   def __init__(self, inputFilename):
     puzutils.CodeJamProblem.__init__(self, inputFilename)
 
     self.T = None
 
   def load(self):
     """
       input:
 
       T (number of test cases)
 
       A (answer to first question)
       x x x x
       x x x x
       x x x x
       x x x x
       B (answer to second question)
       x x x x
       x x x x
       x x x x
       x x x x
 
     """
 
     self.tests = []
 
     with open(self.inputFilename, "rt") as file:
       self.T = int(file.readline().strip())
 
       for i in xrange(self.T):
         a = int(file.readline().strip())
         test = {'a': a}
         board = []
         
         for j in xrange(4):
           line = file.readline().strip()
           row = set([int(x) for x in line.split(' ')])
           board.append(row)
 
         test['aboard'] = board
 
         b = int(file.readline().strip())
         test['b'] = b
         board = []
         
         for j in xrange(4):
           line = file.readline().strip()
           row = set([int(x) for x in line.split(' ')])
           board.append(row)
 
         test['bboard'] = board
 
         self.tests.append(test)
 
     return True
 
   def executeTest(self, test):
     """
       Run a test and return output.
     """
 
     #print "Test: %s\n" % (test, )
 
     rowA = test['aboard'][test['a'] - 1]
     rowB = test['bboard'][test['b'] - 1]
 
     #print "rowA: %s\nrowB: %s\n" % (rowA, rowB)
 
     intersect = rowA.intersection(rowB)
 
     #print "intersect: %s\n" % (intersect, )
 
     if (len(intersect) == 1):
       (element,) = intersect
       return element
     elif (len(intersect) == 0):
       return "Volunteer cheated!"
     else:
       return "Bad magician!"
 
 with Magic_2014_QA(sys.argv[1]) as problem:
   problem.load()
 
   problem.run()
