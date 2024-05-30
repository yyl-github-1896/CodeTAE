#!/usr/bin/python
 
 import sys
 import functools
 import operator
 
 
 def solve(a,b):
     num_recycled = 0
     for n in range(a, b+1):
         s = str(n)
         pairs = []
         for i in range(1,len(s)):
             m = int(s[i:] + s[:i])
             #print("checking " + str(m))
             if n < m and m <= b and m not in pairs:
                 num_recycled += 1
                 pairs.append(m)
     return num_recycled
         
 
 def main():
     N = int(sys.stdin.readline()) # number of testcases
     for i in range(N):
         [a, b] = [int(x) for x in sys.stdin.readline().split()]
         result = solve(a,b)
         print ("Case #%s: %s" % (i+1, result))
 
 
 if __name__ == '__main__':
     main()
