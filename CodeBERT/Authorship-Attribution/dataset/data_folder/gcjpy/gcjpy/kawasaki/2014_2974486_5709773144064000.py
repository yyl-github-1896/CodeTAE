# -*- coding: utf-8 -*-
 
 T = int(raw_input())
 for test_case in xrange(1, T + 1):
     C, F, X = map(float, raw_input().split())
     answer = X / 2
     i = 0
     last_tc = 0
     while True:
         tc = last_tc + C / (2 + (i * F))
         if answer < tc:
             break
         answer = min(tc + X / (2 + (i + 1) * F), answer)
 
         i += 1
         last_tc = tc
     print 'Case #{}: {:.7f}'.format(test_case, answer)
