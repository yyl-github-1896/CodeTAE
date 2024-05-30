#!/usr/bin/env python3
 # -*- encoding: utf-8 -*-
 
 from math import sqrt
 
 def is_palindromic(i):
     n = i
     rev = 0
     while i > 0:
         dig = i % 10
         rev = rev * 10 + dig
         i = i // 10
     return n == rev
 
 def is_square(i):
     if i == 1:
         return True
     x = i // 2
     seen = set([x])
     while x * x != i:
         x = (x + (i // x)) // 2
         if x in seen:
             return False
         seen.add(x)
     return True
 
 def f(a, b):
     tot = 0
 
     sra = a
     while not is_square(sra):
         sra += 1
     srb = b
     while not is_square(srb):
         srb -= 1
 
     sra = int(sqrt(sra))
     srb = int(sqrt(srb))
 
     for i in range(sra, srb+1):
         if is_palindromic(i) and is_palindromic(i ** 2):
             tot += 1
 
     return tot
 
 if __name__ == '__main__':
     T = int(input())
     for i in range(T):
         a, b = map(int, input().split())
         r = f(a, b)
         print('Case #{}: {}'.format(i+1, r))
