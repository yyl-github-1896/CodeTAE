"""Usage:
     pypy X.py < X-size.in > X-size.out
 or sometimes
     python X.py < X-size.in > X-size.out
 """
 
 def setup(infile):
     #C = {}
     return locals()
 
 def reader(testcase, infile, C=None, **ignore):
     N = int(infile.next())
     P = map(float, infile.next().split())
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
 
     N = sorted(P)
     K = sorted(I)
 
     W = 0
     ik = 0
     for n in N:
         while ik < len(K) and K[ik] < n:
             ik += 1
             W += 1
         ik += 1
 
     D = 0
     i = 0
     for k in K:
         while i < len(N) and N[i] < k:
             i += 1
         i += 1
         if i <= len(N):
             D += 1
 
     return 'Case #%s: %s %s\n' % (testcase, D, W)
 
 if __name__ == '__main__':
     import sys
     T = int(sys.stdin.next())
     common = setup(sys.stdin)
     for t in xrange(1, T+1):
         sys.stdout.write(solver(**reader(t, **common)))
