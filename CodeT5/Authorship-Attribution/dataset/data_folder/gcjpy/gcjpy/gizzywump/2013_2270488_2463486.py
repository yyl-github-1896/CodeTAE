#!/usr/bin/env python
 
 import collections
 
 import pickle
 import re
 import sys
 
 INPUT = "tiny"
 if 1:
     INPUT = "C-small-attempt0.in"
 
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
 
 def is_palindrome(N):
     s = str(N)
     return s == ''.join(reversed(s))
 
 def fair_and_square_set(max_N):
     p = "squareset_%d" % max_N
     try:
         s = pickle.load(file(p))
         return s
     except:
         pass
     s = set()
     for i in range(1,max_N+1):
         if is_palindrome(i) and is_palindrome(i*i):
             s.add(i*i)
     pickle.dump(s, file(p, "wb"))
     return s
 
 MAX_N = int(1e7)
 SQUARE_SET = fair_and_square_set(MAX_N)
 #print(SQUARE_SET)
 
 def do_trial(A, B):
     count = 0
     for ss in SQUARE_SET:
         if A <= ss <= B:
             count += 1
     return count
 
 f = file(INPUT)
 T = int(f.readline()[:-1])
 for i in range(T):
     A, B = [int(x) for x in f.readline().split()]
     v = do_trial(A, B)
     print "Case #%d: %s" % (i+1, v)
