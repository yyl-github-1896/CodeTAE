#!/usr/bin/python
 
 import sys
 import math
 import copy
 import operator
 
 f = open(sys.argv[1],'r')
 
 num = int(f.readline())
 
 for i in range(num):
     l = f.readline()
     n,m = l.split()
     n = int(n)
     m = int(m)
     lawn = []
     seen = []
     for j in range(n):
         l = f.readline()
         lawn.append([int(x) for x in l.split()])
         seen.append([False]*m)
     #print lawn
     l = []
     for j in range(n):
         for k in range(m):
             l.append((lawn[j][k], (j,k)))
     l.sort(key=operator.itemgetter(0))
     #print l
     ok = True
     for x in l:
         if seen[x[1][0]][x[1][1]]:
             continue
         row = True
         for j in range(n):
             if not (seen[j][x[1][1]] or lawn[j][x[1][1]] <= lawn[x[1][0]][x[1][1]]):
                 row = False
                 break
         if(row):
             for j in range(n):
                 seen[j][x[1][1]] = True
             continue
         col = True
         for j in range(m):
             if not (seen[x[1][0]][j] or lawn[x[1][0]][j] <= lawn[x[1][0]][x[1][1]]):
                 col = False
                 break
         if(col):
             for j in range(m):
                 seen[x[1][0]][j] = True
             continue
         ok = False
         break
     if ok:
         print 'Case #{}: YES'.format(i+1)
     else:
         print 'Case #{}: NO'.format(i+1)
