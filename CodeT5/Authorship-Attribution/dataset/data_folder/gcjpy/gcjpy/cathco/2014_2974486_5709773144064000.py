import sys
 import time as tm
 sys.setrecursionlimit(15000)
 
 def solve(C, F, X, rate, time):
   if (time + (X / rate)) < ((C / rate) + ((X / (rate+F)) + time)):
     return time + (X / rate)
   else:
     return solve(C, F, X, rate+F, time + (C / rate))
 
 T = int(raw_input())
 for t in range(T):
   C, F, X = map(float, raw_input().split())
   print 'Case #%i: %.7f' % (t+1, solve(C, F, X, 2, 0))
