#!/usr/bin/python
 
 import sys
 import re
 import math
 
 def permute(x, d):
     perm = []
     for i in range(1,d):
         n = x / 10**i
         r = x % 10**i
         #print 'p', i, n, r
         if r >= 10**(i-1):
             perm.append(r * 10**(d-i) + n)
     perm = list(set(perm))
     while x in perm:
         perm.remove(x)
     return perm
 
 f = open(sys.argv[1],'r')
 
 num = int(f.readline())
 
 for i in range(num):
     n1, n2 = [int(x) for x in f.readline().split()]
     d = int(math.floor(math.log10(n1))) + 1
     rec = 0
     for j in range(n1,n2+1):
         p = permute(j, d)
         #print j,p
         rec += sum([1 for x in p if x >= n1 and x <= n2])
         #print rec
     print 'Case #{}:'.format(i+1), rec/2
