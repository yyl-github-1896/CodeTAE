#!/usr/bin/env python
 
 import collections
 
 import re
 import sys
 
 INPUT = "tiny"
 if 1:
     INPUT = "A-small-attempt0.in"
 
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
 
 def check(board, x, y, dx, dy):
     #import pdb; pdb.set_trace()
     c = collections.Counter((board[x+dx*i][y+dy*i] for i in range(4)))
     if c.get("X", 0) + c.get("T", 0) == 4: return "X won"
     if c.get("O", 0) + c.get("T", 0) == 4: return "O won"
 
 def do_trial(board):
     #return "X won" #(the game is over, and X won)
     #"O won" (the game is over, and O won)
     #"Draw" (the game is over, and it ended in a draw)
     #"Game has not completed" (the game is not over yet)
     for x in range(4):
         v = check(board, x, 0, 0, 1)
         if v: return v
         v = check(board, 0, x, 1, 0)
         if v: return v
     v = check(board, 0, 0, 1, 1)
     if v: return v
     v = check(board, 3, 0, -1, 1)
     if v: return v
     if '.' in ''.join(board):
         return "Game has not completed"
     return "Draw"
 
 f = file(INPUT)
 T = int(f.readline()[:-1])
 for i in range(T):
     lines = [f.readline()[:-1] for j in range(4)]
     f.readline()
     v = do_trial(lines)
     print "Case #%d: %s" % (i+1, v)
