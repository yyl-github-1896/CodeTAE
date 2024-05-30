# python 3
 import string
 import itertools
 import sys
 
 def gen_rotations(num):
     digits = [ch for ch in str(num)]
     for i in range(1, len(digits)):
         if digits[i] != '0':
             result = 0
             for d in digits[i:]:
                 result = 10*result + ord(d) - ord('0')
             for d in digits[:i]:
                 result = 10*result + ord(d) - ord('0')
             if result == num:
                 return
             yield result
     
 def process_case(a,b):
     result = 0
     for n in range(a,b+1):
         for m in gen_rotations(n):
             if (n < m <= b):
                 result += 1
     return result
 
 def result_gen(lines):
     ncases = int(next(lines))
     for ci in range(1,ncases+1):
         a,b = line_of_numbers(next(lines))
         result = process_case(a,b)
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
 
 ##start('C-test')
 start('C-small-attempt0')
 ##start('C-large')
