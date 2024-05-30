#!/usr/bin/python
 
 import sys
 import functools
 import operator
 import math
 from itertools import chain, combinations
 from heapq import heappop, heappush, _siftup
 
 def solve(C, F, X):
     rate = 2.0
     time_to_win = X / rate
 
     time_used = C / rate
     rate += F
     time_to_win_new = time_used + X / rate
 
     while time_to_win_new < time_to_win:
         time_to_win = time_to_win_new
         
         time_used += C / rate
         rate += F
         time_to_win_new = time_used + X / rate
 
     return time_to_win
 
 def main():
     N = int(sys.stdin.readline()) # number of testcases
     for i in range(N):
         [C, F, X] = [float(x) for x in sys.stdin.readline().rstrip().split()]
 
         result = solve(C, F, X)
         print ("Case #%s: %.7f" % (i+1, result))
 
 if __name__ == '__main__':
     main()
