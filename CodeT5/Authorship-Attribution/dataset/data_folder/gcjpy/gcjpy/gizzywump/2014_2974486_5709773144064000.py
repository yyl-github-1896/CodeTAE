#!/usr/bin/env python
 
 import collections
 
 import math
 import re
 import sys
 
 sys.setrecursionlimit(5000)
 
 INPUT = "tiny"
 INPUT = "B-large.in"
 INPUT = "B-small-attempt0.in"
 
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
 
 def do_trial(C, F, X, rate=2.0):
     #import pdb; pdb.set_trace()
     win_time_wait = X / rate
     buy_time = C / rate
     win_time_buy_1 = buy_time + X / (rate+F)
     if win_time_wait < win_time_buy_1:
         return win_time_wait
     return buy_time + do_trial(C, F, X, rate+F)
 
 f = file(INPUT)
 T = int(f.readline()[:-1])
 for i in range(T):
     C, F, X = [float(x) for x in f.readline().split()]
     v = do_trial(C, F, X)
     print "Case #%d: %s" % (i+1, v)
