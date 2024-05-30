# -*- coding: utf-8 -*-
 
 import sys
 
 def is_palindrome(num):
     s1 = str(num)
     s2 = s1[::-1]
     return s1 == s2
 
 fair_numbers = []
 for i in range(pow(10, 7)+1):
     if is_palindrome(i):
         num = i*i
         if is_palindrome(num):
             fair_numbers.append(num)
 
 N = int(sys.stdin.readline())
 for T in range(1, N+1):
     min_val, max_val = map(int, sys.stdin.readline().strip().split())
 
     ans = 0
     for num in fair_numbers:
         if num < min_val:
             continue
         if num > max_val:
             break
         ans += 1
     print 'Case #%(T)s: %(ans)s' % locals()
