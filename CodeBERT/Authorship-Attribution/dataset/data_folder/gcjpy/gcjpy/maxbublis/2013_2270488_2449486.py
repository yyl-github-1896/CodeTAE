#!/usr/bin/env python
 import sys
 
 
 def solve_problem(lawn, size_x, size_y):
     for i in xrange(size_x):
         for k in xrange(size_y):
             elem = lawn[i][k]
             if max(lawn[i]) > elem and max([lawn[j][k] for j in xrange(size_x)]) > elem:
                 return 'NO'
 
     return 'YES'
 
 def read_lawn(stdin, size_x, size_y):
     lawn = []
     for i in xrange(size_x):
         line = map(int, sys.stdin.readline().strip().split(' '))
         lawn.append(line)
     return lawn
 
 
 if __name__ == '__main__':
     num_of_cases = int(sys.stdin.readline())
     for i in xrange(1, num_of_cases + 1):
         size_x, size_y = map(int, sys.stdin.readline().strip().split(' '))
         lawn = read_lawn(sys.stdin, size_x, size_y)
         print 'Case #{0}: {1}'.format(i, solve_problem(lawn, size_x, size_y))
