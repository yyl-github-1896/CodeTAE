#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem C. Fair and Square
 # https://code.google.com/codejam/contest/2270488/dashboard#s=p2
 #
 
 import sys
 import math
 
 
 def ispalindrome(n):
     return str(n) == str(n)[::-1]
 
 
 def solve(A, B):
     solution = []
     for n in range(int(math.sqrt(A)), int(math.sqrt(B))+1):
         if ispalindrome(n):
             m = n ** 2
             if ispalindrome(m) and A <= m <= B:
                 solution.append(n)
     return len(solution)
 
 
 def main(IN, OUT):
     T = int(IN.readline())
     for index in range(T):
         A, B = map(int, IN.readline().split())
         OUT.write('Case #%d: %s\n' % (index + 1, solve(A, B)))
 
 
 def makesample(T=100, ABmax=1000):
     import random
     print T
     for index in range(T):
         A = random.randint(1, ABmax)
         B = random.randint(A, ABmax)
         print A, B
 
 
 if __name__ == '__main__':
     if '-makesample' in sys.argv[1:]:
         makesample()
     else:
         main(sys.stdin, sys.stdout)
 
