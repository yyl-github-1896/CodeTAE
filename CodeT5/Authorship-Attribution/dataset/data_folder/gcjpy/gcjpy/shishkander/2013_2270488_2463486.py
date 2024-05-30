import itertools, sys, os
 from itertools import *
 import time, heapq
 
 def pal(s):
     for i in xrange(len(s)/2):
         if s[i] != s[-i-1]:
             return False
     return True
 
 def pal2(x, s):
     return pal(s) and pal(str(x*x))
 
 def E(k):
     return 10**k
 
 
 def CREATE_DATABASE(MAX):
     def init():
         yield 1
         yield 2
         yield 3
         yield 11
         yield 22
         for i in xrange(1, MAX):
             yield 1*E(2*i) + 1
             yield 1*E(2*i+1) + 1
             #yield 1*E(2*i + 1) + 1
             #yield 1*E(2*i) + 1 + 2*E(i)
             yield 2*E(2*i) + 2
             yield 2*E(2*i) + 2 + 1*E(i)
             yield 2*E(2*i+1) + 2
             
             
     heap = list(sorted(set(init())))
     for i in heap:
         print i
     heapq.heapify(heap)
     RES = []
     try:
         MAX_X = E(MAX)
         print "MAX_X", MAX_X
         while True:
             x = heapq.heappop(heap)
             #print x
             RES.append(x)
             if x == 3:
                 continue
             if x > MAX_X:
                 break
             s = str(x)
             j = len(s) / 2
             shift = 1 if len(s) == 2*j else 0
             for i in xrange(j+1, MAX):
                 n = E(2*i-shift) + 1 + E(i-j) * x
                 if pal2(n,str(n)):
                     #print ("{:^%i} => {:^%i}" % (2*MAX, 2*MAX)).format(x, n)
                     heapq.heappush(heap, n)
                 
     except KeyboardInterrupt:
         print "stopped while x is", x
     with open("c.database", 'w') as f:
         for i in sorted(RES + heap):
             f.write("%i\n"%i)
 
 def READ_DATABASE():
     with open("c.database", 'r') as f:
         return sorted(map(lambda x: int(x.strip())**2, f))
 DB = READ_DATABASE()
 
 from bisect import bisect_left, bisect_right
 def CASE(IN):
     def rstr(): return IN.readline().strip()
     def rint(): return int(rstr())
     def rints(): return map(int, rstr().split())
     def nrints(N): return [rints() for i in xrange(N)]
     A, B = rints()
     i = bisect_left(DB, A) 
     j = bisect_right(DB, B)
     return j-i
 
 def RUN(IN, OUT):
     t = int(IN.readline().strip())
     for i in xrange(1,t+1):
         OUT.write("Case #%i: %s\n" % (i, CASE(IN)))
 
 if __name__ == "__main__":
     # CREATE_DATABASE(52)
     import sys
     RUN(sys.stdin, sys.stdout)
