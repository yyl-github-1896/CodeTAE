#!/usr/bin/python
 
 import sys
 
 import puzutils
 
 class War_2014_QD(puzutils.CodeJamProblem):
   def __init__(self, inputFilename):
     puzutils.CodeJamProblem.__init__(self, inputFilename)
 
     self.T = None
 
   def load(self):
     """
       input:
 
       T (number of test cases)
 
       N (number of blocks)
       N1 N2 N3 ... (mass of Naomi's blocks, real)
       K1 K2 K3 ... (mass of Ken's blocks, real)
 
     """
 
     self.tests = []
 
     with open(self.inputFilename, "rt") as file:
       self.T = int(file.readline().strip())
 
       for i in xrange(self.T):
         N = int(file.readline().strip())
         naomi = [float(x) for x in file.readline().split(' ')]
         ken = [float(x) for x in file.readline().split(' ')]
 
         test = {'N': N, 'Naomi': naomi, 'Ken': ken}
 
         self.tests.append(test)
 
     return True
 
   def playWar(self, naomi, ken):
     """
       How many points does naomi get when playing standard War?
     """
 
     if (len(naomi) <= 0):
       return 0
 
     # Just choose the biggest?
     maxN = max(naomi)
 
     # Can ken win?
     maxK = max(ken)
 
     if maxK > maxN:
       # Ken uses the smallest one that will beat her
       k = min([x for x in ken if x > maxN])
 
       #print "Ken wins (%.3f > %.3f), max %.3f" % (k, maxN, maxK)
 
       naomi.remove(maxN)
       ken.remove(k)
 
       return 0 + self.playWar(naomi, ken)
     else:
       # Ken loses his smallest
       k = min(ken)
 
       #print "Ken loses (%.3f < %.3f), max %.3f" % (k, maxN, maxK)
 
       naomi.remove(maxN)
       ken.remove(k)
 
       return 1 + self.playWar(naomi, ken)
 
   def playDWar(self, naomi, ken):
     """
       How many points does naomi get when playing decietful war?
     """
 
     if (len(naomi) <= 0):
       return 0
 
     minN = min(naomi)
     minK = min(ken)
     maxK = max(ken)
 
     if (minN < minK):
       # This is a guaranteed loser, take a big one down with it
       naomi.remove(minN)
       ken.remove(maxK)
       return 0 + self.playDWar(naomi, ken)
 
     # Use our smallest one to beat his smallest one, by lying and
     # saying ours is bigger than his biggest
     naomi.remove(minN)
     ken.remove(minK)
     return 1 + self.playDWar(naomi, ken)
 
   def executeTest(self, test):
     """
       Run a test and return output.
     """
 
     dwar = self.playDWar(list(test['Naomi']), list(test['Ken']))
     war = self.playWar(list(test['Naomi']), list(test['Ken']))
     return "%d %d" % (dwar, war)
 
 with War_2014_QD(sys.argv[1]) as problem:
   problem.load()
 
   problem.run()
