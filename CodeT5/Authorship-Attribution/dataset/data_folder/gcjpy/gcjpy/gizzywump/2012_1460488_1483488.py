#!/usr/bin/env python
 
 import pdb
 import re
 import sys
 
 INPUT = "tiny"
 
 INPUT = "C-small-attempt0.in.txt"
 
 def debug(*args):
     pass #print str(args)
 
 if 0:
     def debug(*args):
         sys.stderr(''.join(str(s) for s in args) + "\n")
 
 def recycleables(N, A, B):
     t = set()
     s = str(N)
     for i in range(len(s)):
         s1 = int(s[i:] + s[:i])
         if A <= s1 <= B:
             t.add(s1)
     return t
 
 def do_trial(A, B):
     total = 0
     seen = set()
     for i in xrange(A, B+1):
         if i not in seen:
             t = recycleables(i, A, B)
             z = len(t)
             total += z * (z-1) / 2
             seen.update(t)
     return total
 
 f = file(INPUT)
 T = int(f.readline()[:-1])
 for i in range(T):
     A, B = [int(x) for x in f.readline()[:-1].split()]
     v = do_trial(A, B)
     print "Case #%d: %s" % (i+1, v)
