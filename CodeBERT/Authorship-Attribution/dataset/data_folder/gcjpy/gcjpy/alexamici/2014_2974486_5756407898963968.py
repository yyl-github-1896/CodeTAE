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
     #P = int(infile.next())
     #P = map(int, infile.next().split())
     I = [map(int, infile.next().split()) for i in range(4)]
     T = int(infile.next())
     #T = infile.next().split()
     S = [map(int, infile.next().split()) for i in range(4)]
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
 
     res = set(I[N-1]) & set(S[T-1])
     if len(res) == 1:
         res = res.pop()
     elif len(res) > 1:
         res = 'Bad magician!'
     else:
         res = 'Volunteer cheated!'
     return 'Case #%s: %s\n' % (testcase, res)
 
 if __name__ == '__main__':
     import sys
     T = int(sys.stdin.next())
     common = setup(sys.stdin)
     for t in xrange(1, T+1):
         sys.stdout.write(solver(**reader(t, **common)))
