#!/usr/bin/python
 
 import sys
 import re
 import math
 import string
 
 f = open(sys.argv[1],'r')
 
 num = int(f.readline())
 
 def count(z, r, c):
     return len(z_and_nei(z,r,c))
 
 def nei(z, r, c):
     s = z_and_nei(z, r, c)
     s -= set(z)
     return s
 
 def z_and_nei(z, r, c):
     s = set()
     for x in z:
         s.add(x)
         s.add((x[0]-1,x[1]-1))
         s.add((x[0]-1,x[1]))
         s.add((x[0]-1,x[1]+1))
         s.add((x[0],x[1]-1))
         s.add((x[0],x[1]+1))
         s.add((x[0]+1,x[1]-1))
         s.add((x[0]+1,x[1]))
         s.add((x[0]+1,x[1]+1))
     o = set()
     for x in s:
         if x[0] < 0 or x[0] > r-1 or x[1] < 0 or x[1] > c-1:
             o.add(x)
     s-=o
     return s
 
 def find_config(z, r, c, t):
     if count(z,r,c) == t:
         return z
     if count(z,r,c) > t:
         return []
     n = nei(z,r,c)
     for x in n:
         z.append(x)
         if find_config(z,r,c,t) != []:
             return z
         z.pop()
     return []
 
 for i in range(num):
     print 'Case #{}:'.format(i+1)
     r, c, m = [int(x) for x in f.readline().split()]
     if r*c-m == 1:
         print 'c' + '*'*(c-1)
         for i in range(r-1):
             print '*'*c
     else:
         z = find_config([(0,0)], c, r, c*r-m)
         if z == []:
             print "Impossible"
         else:
             s = z_and_nei(z, c, r)
             for j in range(r):
                 for k in range(c):
                     if j == 0 and k == 0:
                         print 'c',
                     elif (k,j) in s:
                         print '.',
                     else:
                         print '*',
                 print
 
 
