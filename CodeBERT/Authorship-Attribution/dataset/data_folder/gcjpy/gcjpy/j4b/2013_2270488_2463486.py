#!/usr/bin/python
 
 import sys
 import functools
 import operator
 import math
 
 def isPal(n):
     l = str(n)
     return l == l[::-1]
 
 def solve(a, b):
     l = int(math.ceil(math.sqrt(a)))
     u = int(math.floor(math.sqrt(b)))
 
     count = 0
     for x in range(l, u + 1):
         if isPal(x):
             if isPal(x*x):
                 count += 1
     return str(count)
 
 def main():
     N = int(sys.stdin.readline()) # number of testcases
     for i in range(N):
         [a,b] = [int(x) for x in sys.stdin.readline().rstrip().split()]
         result = solve(a, b)
         print ("Case #%s: %s" % (i+1, result))
 
         # use something like:
         # sys.stdin.readline()
         # [int(x) for x in sys.stdin.readline().split()]
 
 
 if __name__ == '__main__':
     main()
