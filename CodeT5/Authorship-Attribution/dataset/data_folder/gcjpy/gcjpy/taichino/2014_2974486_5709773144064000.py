# -*- coding: utf-8 -*-
 
 import sys
 
 N = int(sys.stdin.readline())
 
 for T in range(1, N+1):
     C, F, X = map(float, sys.stdin.readline().split(' '))
 
     # find N
     N = 0
     for i in range(int(X)):
         diff = (2 + F * i) * C - F * X
         if diff >= 0: break
         N = i
 
     # calc seconds
     total = 0
     for i in range(N):
         val = C / (2 + i * F)
         total += val
     val = X / (2.0 + N * F)
     total += val
         
     ans = '%s' % (total)
     print 'Case #%(T)s: %(ans)s' % locals()
