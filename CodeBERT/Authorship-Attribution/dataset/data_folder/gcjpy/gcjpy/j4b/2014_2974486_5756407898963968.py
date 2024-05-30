#!/usr/bin/python
 
 import sys
 import functools
 import operator
 import math
 from itertools import chain, combinations
 from heapq import heappop, heappush, _siftup
 
 def solve(row1, row2):
     common = [x for x in row1 if x in row2]
     num_common = len(common)
     if num_common == 0:
         return 'Volunteer cheated!'
     elif num_common > 1:
         return 'Bad magician!'
     else:
         return common[0]
 
 def main():
     N = int(sys.stdin.readline()) # number of testcases
     for i in range(N):
         row_index1 = int(sys.stdin.readline())
         row1 = list()
         for j in range(4):
             if row_index1 == j + 1:
                 row1 = [int(x) for x in sys.stdin.readline().rstrip().split()]
             else:
                 sys.stdin.readline()
 
         row_index2 = int(sys.stdin.readline())
         row2 = list()
         for j in range(4):
             if row_index2 == j + 1:
                 row2 = [int(x) for x in sys.stdin.readline().rstrip().split()]
             else:
                 sys.stdin.readline()
 
         result = solve(row1, row2)
         print ("Case #%s: %s" % (i+1, result))
 
 if __name__ == '__main__':
     main()
