#!/usr/bin/python
 
 import sys
 import functools
 import operator
 import math
 from itertools import chain, combinations
 from heapq import heappop, heappush, _siftup
 
 def solveWar(n_weights, k_weights):
     nweights = sorted(n_weights)
     kweights = sorted(k_weights)
     score = 0
     
     # while nweights:
     #     w = nweights.pop(0)
     #     res = [kweight for kweight in kweights if kweight > w]
     #     if res:
     #         kweights.remove(min(res))
     #     else:
     #         score += len(nweights) + 1
     #         break
 
     for w in nweights:
         while kweights and kweights[0] < w:
             kweights.pop(0)
             score += 1
 
         if not kweights:
             break
         else:
             kweights.pop(0)
             
     return score
 
 def solveDWar(n_weights, k_weights):
     nweights = sorted(n_weights)
     kweights = sorted(k_weights)
     score = 0
 
     for w in nweights:
         if w > kweights[0]:
             score += 1
             kweights.pop(0)
         else:
             kweights.pop(-1)
     
     return score
 
 def solve(nweights, kweights):
     return ("%s %s" % (solveDWar(nweights, kweights), solveWar(nweights, kweights)))
 
 def main():
     N = int(sys.stdin.readline()) # number of testcases
     for i in range(N):
         sys.stdin.readline()
         nweights = [float(x) for x in sys.stdin.readline().rstrip().split()]
         kweights = [float(x) for x in sys.stdin.readline().rstrip().split()]
 
         result = solve(nweights, kweights)
         print ("Case #%s: %s" % (i+1, result))
 
 if __name__ == '__main__':
     main()
