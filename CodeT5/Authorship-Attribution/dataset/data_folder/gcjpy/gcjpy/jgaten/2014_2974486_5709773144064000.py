#!/usr/bin/env python
 
 import sys
 
 def solve(c, f, x):
     time = 0
     cps = 2.0
     while True:
         time_to_farm = c / cps
         time_to_end = x / cps
         buy_a_farm = (time_to_farm + x / (cps + f)) < time_to_end
         #print time_to_farm, time_to_end, (time_to_farm + x / (cps + f)), buy_a_farm
         if buy_a_farm:
             time += time_to_farm
             cps += f
         else:
             time += time_to_end
             return time
 
 if __name__ == '__main__':
     fin = open(sys.argv[1], 'rU') if sys.argv[1:] else sys.stdin
     fout = open(sys.argv[2], 'w') if sys.argv[2:] else sys.stdout
     with fin, fout:
         T = int(fin.readline())
         for case in xrange(1, T+1):
             c, f, x = map(float, fin.readline().split())
             soln = solve(c, f, x)
             print >> fout, "Case #{0}: {1:.7f}".format(case, soln)
 
