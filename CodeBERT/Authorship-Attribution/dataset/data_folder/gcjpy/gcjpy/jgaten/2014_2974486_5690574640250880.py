#!/usr/bin/env python
 
 import sys
 
 IMPOSSIBLE = []
 
 def transpose(grid):
     return map(list, zip(*grid))
 
 def find_grid(R, C, M):
     """Return a grid of a solution, if one exists, otherwise []
 
     Observations:
     * WLOG, C <= R (otherwise, take the transpose of a solution)
     * Trivial cases are:
       - M = 0 or  M = RC - 1
       - C = 1
       - (R, C) = (2, 2)
       - (R, C, M) = (3, 3, 2)
       - (C, M) = (2, 1)
     * If M >= C >= 2 and R >= 3, we can add a row of C mines to the bottom and consider M'=M-C, R'=R-1
     * The remaining cases are M <= R-2, and M + 1 == R == C >= 4, which are both solvable
     """
     # Take care of simple cases
     if M == 0:
         #print "zero ", R, C, M
         grid = [['.' for c in xrange(C)] for r in xrange(R)]
         grid[0][0] = 'c'
         return grid
     elif M == R * C - 1:
         #print "full ", R, C, M
         grid = [['*' for c in xrange(C)] for r in xrange(R)]
         grid[0][0] = 'c'
         return grid
     elif C > R:
         #print "trans", R, C, M
         return transpose(find_grid(C, R, M))
     elif C == 1:
         #print "C=1  ", R, C, M
         return [['c']] + [['.'] for i in xrange(R-M-1)] + [['*'] for i in xrange(M)]
     elif (R, C) == (2, 2) or (R, C, M) == (3, 3, 2) or (C, M) == (2, 1):
         #print "impos", R, C, M
         return IMPOSSIBLE
 
     assert 2 <= C <= R >= 3, "R={} C={} M={}".format(R, C, M)
 
     if M >= C:
         #print "M>=C ", R, C, M
         s = find_grid(R-1, C, M-C)
         return s and s + [['*' for c in xrange(C)]]
     elif M <= R-2 and C >= 3:
         #print "M+1<R", R, C, M
         grid = [['.' for c in xrange(C)] for r in xrange(R)]
         grid[0][0] = 'c'
         for i in xrange(M):
             grid[R-i-1][C-1] = '*'
         return grid
     elif M + 1 == R == C >= 4:
         #print "M+1=R", R, C, M
         grid = [['.' for c in xrange(C)] for r in xrange(R)]
         grid[0][0] = 'c'
         grid[R-1][C-2] = '*'
         for i in xrange(M-1):
             grid[R-i-1][C-1] = '*'
         return grid
 
     assert False, "R={} C={} M={}".format(R, C, M)
 
 def check_soln(grid, R, C, M):
     """checking, because debugging..."""
     error = "R={} C={} M={}".format(R, C, M)
     assert sum(row.count('*') for row in grid) == M, error
     assert sum(row.count('c') for row in grid) == 1, error
     assert len(grid) == R, error
     assert all(len(row) == C for row in grid), error
     _ = [i for i, row in enumerate(grid) if 'c' in row][0]
     click = (_, [i for i, c in enumerate(grid[_]) if c == 'c'][0])
 
     def neighbours(r, c):
         ns = [(i, j) for i in range(max(r-1,0),min(r+2,R)) for j in range(max(c-1,0),min(c+2,C))]
         ns.remove((r, c))
         return ns
 
     cpy = map(list, grid)
     def fill(cpy, pos):
         cpy[pos[0]][pos[1]] = str(sum(1 for i, j in neighbours(*pos) if grid[i][j] == '*'))
         if cpy[pos[0]][pos[1]] == '0':
             for i, j in neighbours(*pos):
                 if cpy[i][j] == '.':
                     fill(cpy, (i, j))
     fill(cpy, click)
     assert sum(row.count('.') for row in cpy) == 0, error
 
 def solve(R, C, M):
     soln = find_grid(R, C, M)
     if soln == IMPOSSIBLE:
         return "Impossible"
     else:
         check_soln(soln, R, C, M)
         return '\n'.join(''.join(row) for row in soln)
 
 if __name__ == '__main__':
     fin = open(sys.argv[1], 'rU') if sys.argv[1:] else sys.stdin
     fout = open(sys.argv[2], 'w') if sys.argv[2:] else sys.stdout
     with fin, fout:
         T = int(fin.readline())
         for case in xrange(1, T+1):
             r, c, m = map(int, fin.readline().split())
             soln = solve(r, c, m)
             print >> fout, "Case #{0}:\n{1}".format(case, soln)
 
