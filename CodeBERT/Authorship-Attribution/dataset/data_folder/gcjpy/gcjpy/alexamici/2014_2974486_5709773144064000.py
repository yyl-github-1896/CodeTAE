"""Usage:
     pypy X.py < X-size.in > X-size.out
 or sometimes
     python X.py < X-size.in > X-size.out
 """
 
 def setup(infile):
     #C = {}
     return locals()
 
 def reader(testcase, infile, C=None, **ignore):
     #N = int(infile.next())
     #P = map(int, infile.next().split())
     I = map(float, infile.next().split())
     #T = infile.next().split()
     #S = [infile.next().strip() for i in range(N)]
     return locals()
 
 def solver(testcase, N=None, P=None, I=None, T=None, S=None, C=None, **ignore):
     #import collections as co
     #import functools32 as ft
     #import itertools as it
     #import operator as op
     #import math as ma
     #import re
     #import numpypy as np
     #import scipy as sp
     #import networkx as nx
 
     C, F, X = I
     n = [0]
     r = 2.
 
     res = X / r
     while True:
         n.append(n[-1] + C / r)
         r += F
         nres = n[-1] + X / r
         if nres >= res:
             break
         res = nres
 
     return 'Case #%s: %s\n' % (testcase, res)
 
 if __name__ == '__main__':
     import sys
     T = int(sys.stdin.next())
     common = setup(sys.stdin)
     for t in xrange(1, T+1):
         sys.stdout.write(solver(**reader(t, **common)))
