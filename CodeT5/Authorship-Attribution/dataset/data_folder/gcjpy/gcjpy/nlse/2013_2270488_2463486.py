#!/usr/bin/python
 
 import sys
 import math
 import copy
 
 f = open(sys.argv[1],'r')
 
 num = int(f.readline())
 
 def pal(x):
     l = list(str(x))
     l2 = copy.copy(l)
     l2.reverse()
     return l == l2
 
 for i in range(num):
     count = 0
     line = f.readline()
     a,b = line.split()
     a = int(a)
     b = int(b)
     ma = int(math.sqrt(a))
     mb = int(math.sqrt(b))+1
     #print a,b
     for j in range(ma,mb+1):
         q = j*j
         if q < a or q > b:
             continue
         #print i*i
         if pal(j) and pal(q):
             #print i,q
             count += 1
     print 'Case #{}:'.format(i+1), count
