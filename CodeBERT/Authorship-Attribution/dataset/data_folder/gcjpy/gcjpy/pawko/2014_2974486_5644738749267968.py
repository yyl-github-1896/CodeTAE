# python 3
 import string
 import itertools
 import sys
 
 def war_points(N, naomi_sorted, ken_sorted):
     j=0
     naomi_points = 0
     for i in range(N):
         while j < N and naomi_sorted[i] > ken_sorted[j]:
             j += 1
         if j < N:
             j += 1
         else:
             naomi_points += 1
     return naomi_points
     
 def deceitful_war_points(N, naomi_sorted, ken_sorted):
     j=0
     naomi_points = 0
     for i in range(N):
         while j < N and ken_sorted[i] > naomi_sorted[j]:
             j += 1
         if j < N:
             naomi_points += 1
             j += 1
     return naomi_points
 
 def process_case(N, naomi_sorted, ken_sorted):
     x1 = deceitful_war_points(N, naomi_sorted, ken_sorted)
     x2 = war_points(N, naomi_sorted, ken_sorted)
     return (x1, x2)
 
 def result_gen(lines):
     ncases = int(next(lines))
     for ci in range(1,ncases+1):
         N = int(next(lines))
         naomi_sorted = line_of_floats_sorted(next(lines))
         ken_sorted = line_of_floats_sorted(next(lines))
         x1, x2 = process_case(N, naomi_sorted, ken_sorted)
         yield 'Case #{0}: {1} {2}\n'.format(ci, x1, x2)
     
 def line_of_floats_sorted(s):
     fv = [float(sub) for sub in s.split()]
     fv.sort()
     return fv
 
 def input_gen(f_in):
     for line in f_in:
         if line.endswith('\n'):
             line = line[:-1]
         yield line
 
 def start(basename):
     infile = basename + '.in'
     outfile = basename + '.out'
     f_in = open(infile, 'r')
     f_out = open(outfile, 'w')
     f_out.writelines(result_gen(input_gen(f_in)))
     f_in.close()
     f_out.close()
 
 ##start('D-test')
 start('D-small-attempt0')
 ##start('D-large')
