#!/usr/bin/python
 # -*- coding: utf-8 -*-
 
 import sys
 
 def recycled_numbers(num):
     result = []
     num_text = str(num)
     for i in range(1, len(num_text)):
         rotated = int(num_text[i:] + num_text[:i])
         if num != rotated:
             result.append(rotated)
     return result
 
 for T, line in enumerate(sys.stdin):
     if T == 0:
         continue
 
     results = []
     params = [int(n) for n in line.split(' ')]
     (A, B) = params
     for i in range(A, B):
         candidates = recycled_numbers(i)
         for c in candidates:
             pair = (i, c)
             if pair not in results and A <= c and c <= B and i < c:
                 results.append(pair)
     # print results
     ans = len(results)
     print 'Case #%(T)s: %(ans)s' % locals()
