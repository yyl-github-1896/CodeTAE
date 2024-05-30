#!/usr/bin/env python
 import sys
 
 def solve(N, M, grid):
     possible = [[False for _ in xrange(M)] for _ in xrange(N)]
     for i in xrange(N):
         m = max(grid[i])
         for j in xrange(M):
             possible[i][j] = possible[i][j] or grid[i][j] == m
 
     for j in xrange(M):
         m = max(grid[_][j] for _ in xrange(N))
         for i in xrange(N):
             possible[i][j] = possible[i][j] or grid[i][j] == m
 
     if all(all(row) for row in possible):
         return "YES"
     else:
         return "NO"
 
 if __name__ == '__main__':
     with open(sys.argv[1], 'rU') as fin, open(sys.argv[2], 'w') as fout:
         T = int(fin.readline())
         for case in xrange(1, T+1):
             print "Case #{0}:".format(case)
 
             N, M = map(int, fin.readline().split())
             grid = [map(int, fin.readline().split()) for _ in xrange(N)]
 
             soln = solve(N, M, grid)
             print soln
             print >> fout, "Case #{0}: {1}".format(case, soln)
