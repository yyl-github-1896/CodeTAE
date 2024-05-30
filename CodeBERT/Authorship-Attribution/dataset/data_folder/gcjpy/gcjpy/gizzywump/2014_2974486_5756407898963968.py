#!/usr/bin/env python
 
 import collections
 
 import math
 import re
 import sys
 
 INPUT = "tiny"
 if 1:
     INPUT = "A-large.in"
     INPUT = "A-small-attempt0.in"
 
 def debug(*args):
     return
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
 
 def do_trial(a1, r1, a2, r2):
     p1 = set(r1[a1-1])
     p2 = set(r2[a2-1])
     u = p1.intersection(p2)
     if len(u) < 1:
         return "Volunteer cheated!"
     if len(u) > 1:
         return "Bad magician!"
     return list(u)[0]
 
 f = file(INPUT)
 T = int(f.readline()[:-1])
 for i in range(T):
     rows1 = []
     a1 = int(f.readline()[:-1])
     for r in range(4):
         rows1.append([int(x) for x in f.readline().split()])
     a2 = int(f.readline()[:-1])
     rows2 = []
     for r in range(4):
         rows2.append([int(x) for x in f.readline().split()])
     v = do_trial(a1, rows1, a2, rows2)
     print "Case #%d: %s" % (i+1, v)
