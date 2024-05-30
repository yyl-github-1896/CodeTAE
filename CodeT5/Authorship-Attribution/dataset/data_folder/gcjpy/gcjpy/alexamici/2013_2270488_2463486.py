"""Usage:
     X.py < X.in > X.out
 """
 
 # http://code.activestate.com/recipes/577821-integer-square-root-function/
 def isqrt(x):
     "returns int(floor(sqrt(x))) using only integer math"
     assert x >= 0, 'Undefined %r' % locals()
     n = int(x)
     if n == 0:
         return 0
     a, b = divmod(n.bit_length(), 2)
     x = 2**(a+b)
     while True:
         y = (x + n//x)//2
         if y >= x:
             return x
         x = y
 
 def setup(infile):
     #C = {}
     return locals()
 
 def reader(testcase, infile, **ignore):
     #N = int(infile.next())
     P = map(int, infile.next().split())
     #I = map(int, infile.next().split())
     #T = infile.next().split()
     #S = [infile.next().strip() for i in range(N)]
     return locals()
 
 def solver(infile, testcase, N=None, P=None, I=None, T=None, S=None, C=None, **ignore):
     #import collections as co
     #import functools as ft
     #import itertools as it
     #import operator as op
     #import math as ma
     #import re
     #import numpy as np
     #import scipy as sp
     #import networkx as nx
 
     low = isqrt(P[0])
     high = isqrt(P[1])+1
 
     def is_pal(n):
         n = str(n)
         for i in range(len(n)/2+1):
             if n[i]!=n[len(n)-1-i]:
                 return False
         return True
 
     res = 0
     for i in range(low, high+1):
         if P[0]<=i*i<=P[1] and is_pal(i) and is_pal(i*i):
             res += 1
 
     return 'Case #%s: %s\n' % (testcase, res)
 
 if __name__ == '__main__':
     import sys
     T = int(sys.stdin.next())
     common = setup(sys.stdin)
     for t in xrange(1, T+1):
         sys.stdout.write(solver(**reader(t, **common)))
