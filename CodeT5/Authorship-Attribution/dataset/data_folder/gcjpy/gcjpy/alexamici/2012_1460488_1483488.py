"""Usage:
     X.py < X.in > X.out
 """
 
 import sys
 
 
 class Solver(object):
     cache = {}
 
     def __init__(self, infile, testcase):
         self.testcase = testcase
         #self.N = N = int(infile.next())
         #self.P = P = map(int, infile.next().split())
         self.I = I = map(int, infile.next().split())
         #self.T = T = infile.next().split()
         #self.S = S = [infile.next().strip() for i in range(N)]
 
         #self.init_cache()
 
     def init_cache(self):
         if 'main' in self.cache:
             return
         #self.cache['main'] = res
 
     def solve(self):
         #import collections as co
         #import functools as ft
         #import itertools as it
         #import operator as op
         #import math as ma
         #import re
         #import numpy as np
         #import scipy as sp
 
         #N = self.N
         #N, M = self.P
         I = self.I
         #T = self.T
         #S = self.S
         l = len(str(I[0]))
 
         r = 0
         for i in xrange(I[0], I[1]):
             ii = str(i)
             rr = set()
             for j in xrange(1, l):
                 if  i < int(ii[j:]+ii[:j]) <= I[1]:
                     rr.add(ii[j:]+ii[:j])
             r += len(rr)
 
         return r
 
 
 def main():
     T = int(sys.stdin.next())
     for t in xrange(T):
         sys.stdout.write('Case #%s: %s\n' % (t + 1, Solver(sys.stdin, t).solve()))
 
 
 if __name__ == '__main__':
     main()
