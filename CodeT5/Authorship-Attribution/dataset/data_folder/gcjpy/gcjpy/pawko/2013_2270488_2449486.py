# python 3
 import string
 import itertools
 import sys
 
 def is_valid(height, max1, max2):
     if height < max1 and height < max2:
         return False
     return True
 
 def process_case(heights):
     nrows = len(heights)
     ncols = len(heights[0])
     col_max_vals = [max((heights[r][c] for r in range(nrows)))
                     for c in range(ncols)]
     row_max_vals = [max((heights[r][c] for c in range(ncols)))
                     for r in range(nrows)]
     for r in range(nrows):
         for c in range(ncols):
             if not is_valid(heights[r][c], row_max_vals[r], col_max_vals[c]):
                 return 'NO'
     return 'YES'
 
 def result_gen(lines):
     ncases = int(next(lines))
     for ci in range(1,ncases+1):
         nrows, ncols = line_of_numbers(next(lines))
         heights = [line_of_numbers(next(lines)) for r in range(nrows)]
         result = process_case(heights)
         yield 'Case #{0}: {1}\n'.format(ci, result)
     
 def line_of_numbers(s):
     return [int(sub) for sub in s.split()]
 
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
