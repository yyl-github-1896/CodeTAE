#!/usr/bin/env python
 
 
 def rotate(i, ndigits):
     s = str(i)
     s = s[-ndigits:] + s[:-ndigits]
     return int(s)
 
 def pairs(A, B):
     for n in range(A, B + 1):
         for i in range(1, len(str(n))):
             m = rotate(n, i)
             if n >= m or m > B: continue
             yield n, m
 
 def main():
     import sys
     with open(sys.argv[1], 'r') as f:
         f.readline()
         n = 0
         for line in f:
             n += 1
 
             A, B = [int(x) for x in line.split(' ')]
             unique = set()
             for pair in pairs(A, B):
                 unique.add(pair)
             print 'Case #%d: %d' % (n, len(unique))
 
 if __name__ == '__main__':
     main()
