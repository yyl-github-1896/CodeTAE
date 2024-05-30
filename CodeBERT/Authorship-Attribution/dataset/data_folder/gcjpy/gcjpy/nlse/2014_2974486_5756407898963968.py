#!/usr/bin/python
 
 import sys
 import re
 import math
 import string
 
 f = open(sys.argv[1],'r')
 
 num = int(f.readline())
 
 for i in range(num):
     q1 = int(f.readline())
     for j in range(4):
         if j+1 == q1:
             line1 = f.readline()
         else:
             f.readline()
     q2 = int(f.readline())
     for j in range(4):
         if j+1 == q2:
             line2 = f.readline()
         else:
             f.readline()
     line1 = [int(x) for x in line1.split()]
     line2 = [int(x) for x in line2.split()]
     count = 0
     for x in line1:
         if x in line2:
             count += 1
             y = x
     if count == 0:
         print 'Case #{}: Volunteer cheated!'.format(i+1)
     elif count == 1:
         print 'Case #{}: {}'.format(i+1, y)
     else:
         print 'Case #{}: Bad magician!'.format(i+1)
