#!/usr/bin/env python
 
 import collections
 
 import re
 import sys
 
 INPUT = "tiny"
 if 1:
     INPUT = "B-small-attempt0.in"
 
 def debug(*args):
     pass #print str(args)
 
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
 
 def do_trial(lawn):
     w = len(lawn[0])
     h = len(lawn)
     x_maxes = [max(lawn_row) for lawn_row in lawn]
     y_maxes = [max(lawn[y][x] for y in range(h)) for x in range(w)]
     def lawn_row(y):
         x_max = x_maxes[y]
         return tuple([min(y_maxes[x], x_max) for x in range(w)])
     new_lawn = tuple([lawn_row(y) for y in range(h)])
     #import pdb; pdb.set_trace()
     if new_lawn == lawn:
         return "YES"
     return "NO"
 
 f = file(INPUT)
 T = int(f.readline()[:-1])
 for i in range(T):
     w, h = [int(x) for x in f.readline().split()]
     lawn = []
     for k in range(w):
         lawn.append(tuple([int(x) for x in f.readline().split()]))
     lawn = tuple(lawn)
     #if i==2:
     #    import pdb; pdb.set_trace()
     v = do_trial(lawn)
     print "Case #%d: %s" % (i+1, v)
