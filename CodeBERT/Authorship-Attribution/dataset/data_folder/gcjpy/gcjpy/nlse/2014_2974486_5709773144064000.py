#!/usr/bin/python
 
 import sys
 import re
 import math
 import string
 
 f = open(sys.argv[1],'r')
 
 num = int(f.readline())
 
 for i in range(num):
     c, e, x = [float(x) for x in f.readline().split()]
     n = int((x*e-2*c)/(c*e))
     if n < 0:
         n = 0
     t = 0
     for j in range(n):
         t += c/(2+j*e)
     t += x/(2+n*e)
     print 'Case #{}: {}'.format(i+1, t)
