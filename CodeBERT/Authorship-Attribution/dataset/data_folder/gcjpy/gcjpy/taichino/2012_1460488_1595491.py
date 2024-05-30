#!/usr/bin/python
 # -*- coding: utf-8 -*-
 
 import sys
 
 for i, line in enumerate(sys.stdin):
     if i == 0:
         continue
 
     params = [int(n) for n in line.split(' ')]
     (N, S, p) = params[:3]
     scores = params[3:]
 
     (clear, possible) = (0, 0)
     normal_min = max(p * 3 - 2, 0)
     suprising_min = max(p * 3 - 4, 0)
     for score in scores:
         if p > score:
             continue
         elif score >= normal_min:
             clear += 1
         elif score >= suprising_min:
             possible += 1
 
     ans = clear + min(possible, S)
     print 'Case #%(i)s: %(ans)s' % locals()
