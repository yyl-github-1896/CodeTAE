#!/usr/bin/python
 
 import sys
 
 import puzutils
 
 class Cookie_2014_QB(puzutils.CodeJamProblem):
   def __init__(self, inputFilename):
     puzutils.CodeJamProblem.__init__(self, inputFilename)
 
     self.T = None
 
   def load(self):
     """
       input:
 
       T (number of test cases)
 
       C F X (real numbers)
 
     """
 
     self.tests = []
 
     with open(self.inputFilename, "rt") as file:
       self.T = int(file.readline().strip())
 
       for i in xrange(self.T):
         (C,F,X) = [float(x) for x in file.readline().split(' ')]
 
         self.tests.append([C,F,X])
 
     return True
 
   def timeToNextFarm(self, C, rate):
     """
       How long in seconds until we get the next farm.
     """
 
     return (C * 1.0) / rate
 
   def timeToTarget(self, C, X, rate):
     """
       How long in seconds until we hit the target.
     """
 
     return ( X * 1.0) / rate
 
   def isFarmWorthIt(self, C, X, F, rate):
     #print "C = %.2f, F = %.2f, X = %.2f, rate = %.2f" % (C, F, X, rate)
 
     withoutFarm = self.timeToTarget(C, X, rate)
     withFarm = self.timeToNextFarm(C, rate) + self.timeToTarget(C, X, rate + F)
 
     #print "With farm = %.2f" % (withFarm,)
     #print "Without farm = %.2f" % (withoutFarm,)
 
     if (withFarm < withoutFarm):
       return True
     else:
       return False
 
   def executeTest(self, test):
     """
       Run a test and return output.
     """
 
     (C,F,X) = test
     rate = 2
     elapsed = 0.0
 
     #print "C = %.2f, F = %.2f, X = %.2f, rate = %.2f" % (C, F, X, rate)
 
     while True:
       if self.isFarmWorthIt(C, X, F, rate):
         #print "%.2f: Bought farm, rate = %d" % (elapsed, rate)
         elapsed = elapsed + self.timeToNextFarm(C, rate)
         rate = rate + F
       else:
         #print "%.2f: Giving up and finishing it out, rate = %d" % (elapsed, rate)
         elapsed = elapsed + self.timeToTarget(C, X, rate)
         return "%0.7f" % (elapsed, )
 
 with Cookie_2014_QB(sys.argv[1]) as problem:
   problem.load()
 
   problem.run()
