# python 3
 import string
 import itertools
 import sys
 
 BASE_RATE = 2.0
 
 def process_case(C, F, X):
     rate = BASE_RATE
     total_time = 0.0
     while True:        
         xtime = X / rate
         ctime = C / rate
         ext_rate = rate + F
         ext_time = ctime + (X / ext_rate)
         if xtime <= ext_time:
             total_time += xtime
             break
         total_time += ctime
         rate = ext_rate
     return total_time
 
 def result_gen(lines):
     ncases = int(next(lines))
     for ci in range(1,ncases+1):
         C, F, X = line_of_floats(next(lines))
         result = process_case(C, F, X)
         yield 'Case #{0}: {1:.7f}\n'.format(ci, result)
 
 def line_of_floats(s):
     return [float(sub) for sub in s.split()]
 
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
 
 ##start('B-test')
 start('B-small-attempt0')
 ##start('B-large')
