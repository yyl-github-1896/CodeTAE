#!/usr/bin/env python
 
 import collections
 
 import math
 import re
 import sys
 
 #sys.setrecursionlimit(50)
 
 INPUT = "tiny"
 #INPUT = "C-large.in"
 INPUT = "C-small-attempt1.in"
 
 def debug(*args):
     #return
     sys.stderr.write(str(args) + "\n")
 
 class Memoize:
     def __init__(self,function):
         self._cache = {}
         self._callable = function
             
     def __call__(self, *args, **kwds):
         cache = self._cache
         key = self._getKey(*args,**kwds)
         try: return cache[key]
         except KeyError:
             cachedValue = cache[key] = self._callable(*args,**kwds)
             return cachedValue
     
     def _getKey(self,*args,**kwds):
         return kwds and (args, ImmutableDict(kwds)) or args    
 
 IMPOSSIBLE = set([(2,2,2), (2,2,1), (2,3,1), (2,4,1), (2,5,1)])
 
 for i in range(2,51):
     IMPOSSIBLE.add((2,i,1))
     IMPOSSIBLE.add((i,2,1))
 
 SOLN = {
     (1,2,1) : ["c*"],
     (2,1,1) : ["c", "*"],
     (2,2,3) : ["c*", "**"],
 }
 
 def solve(R, C, M):
     if M == 0:
         s = ["c%s" % ('.' * (C-1))]
         for i in range(R-1):
             s.append('.' * C)
         return s
     t = (R, C, M)
     if t in IMPOSSIBLE:
         debug("** %s %s %s" % t)
         raise ValueError
     if t in SOLN:
         return SOLN[t]
 
     # last row?
     if C < M and R > 2:
         try:
             return solve(R-1, C, M-C) + ["*" * C]
         except ValueError:
             pass
 
     if C <= R:
         if M >= C and R > 2:
             return solve(R-1, C, M-C) + ["*" * C]
     else:
         if M >= R and C > 2:
             return ["%s*" % s for s in solve(R, C-1, M-R)]
     if R > 2:
         # fill in last row
         mines = min(C, M)
         if mines == C - 1:
             mines -= 1
         try:
             return solve(R-1, C, M-mines) + [("." * (C - mines)) + ("*" * mines)]
         except ValueError:
             if C > 2:
                 mines = min(R, M)
             if mines == R - 1:
                 mines -= 1
             s = ["%s%s" % (s, '*' if k > C-mines else '.') for k, s in enumerate(solve(R, C-1, M-mines))]
             return s
     debug(R, C, M)
     return []
 
 def do_trial(R, C, M):
     try:
         r = solve(R,C,M)
         s = "\n" + '\n'.join(r)
         assert len(r) == R
         for r1 in r:
             assert len(r1) == C
         assert len(''.join(k for k in s if k == '*')) == M
         return s
     except ValueError:
         return "\nImpossible"
 
 
 def all():
     for R in range(1,50):
         for C in range(1,50):
             for M in range(R*C):
                 print(R, C, M)
                 print(do_trial(R, C, M))
     sys.exit(0)
 
 #all()
 
 f = file(INPUT)
 T = int(f.readline()[:-1])
 for i in range(T):
     R, C, M = [int(x) for x in f.readline().split()]
     #import pdb; pdb.set_trace()
     v = do_trial(R, C, M)
     print "Case #%d: %s" % (i+1, v)
