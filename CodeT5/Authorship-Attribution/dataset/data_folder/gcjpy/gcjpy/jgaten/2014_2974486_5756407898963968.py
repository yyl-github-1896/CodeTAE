#!/usr/bin/env python
 
 import sys
 
 def read_row(fin, n):
     rows = [set(map(int, fin.readline().strip().split())) for i in xrange(4)]
     return rows[n-1]
 
 def solve(rowa, rowb):
     both = rowa & rowb
     if len(both) == 1:
         return list(both)[0]
     elif len(both) > 1:
         return "Bad magician!"
     elif not both:
         return "Volunteer cheated!"
 
 if __name__ == '__main__':
     fin = open(sys.argv[1], 'rU') if sys.argv[1:] else sys.stdin
     fout = open(sys.argv[2], 'w') if sys.argv[2:] else sys.stdout
     with fin, fout:
         T = int(fin.readline())
         for case in xrange(1, T+1):
             n = int(fin.readline())
             rowa = read_row(fin, n)
             n = int(fin.readline())
             rowb = read_row(fin, n)
             soln = solve(rowa, rowb)
             print >> fout, "Case #{0}: {1}".format(case, soln)
 
