# python 3
 
 import math
 
 def is_palindrome(num):
     s = str(num)
     end_idx = len(s)-1
     for i in range(len(s)//2):
         if s[i] != s[end_idx-i]:
             return False
     return True
 
 def is_valid_base(base):
     return is_palindrome(base) and is_palindrome(base*base)
 
 def process_case(lo, hi):
     cnt = 0
     base_lo = math.ceil(math.sqrt(lo))
     base_hi = math.floor(math.sqrt(hi))
     for base in range(base_lo, base_hi+1):
         if is_valid_base(base):
             cnt += 1
     return cnt
 
 def result_gen(lines):
     ncases = int(next(lines))
     for ci in range(1,ncases+1):
         lo,hi = line_of_numbers(next(lines))
         result = process_case(lo, hi)
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
