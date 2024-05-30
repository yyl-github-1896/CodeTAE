# python 3
 import string
 import itertools
 import sys
 
 def process_case(row1, tab1, row2, tab2):
     s1 = set(tab1[row1])
     s2 = set(tab2[row2])
     xset = s1 & s2
     if len(xset) == 1:
         result = xset.pop()
     elif len(xset) == 0:
         result = 'Volunteer cheated!'
     else:
         result = 'Bad magician!'
     return result
 
 def result_gen(lines):
     ncases = int(next(lines))
     for ci in range(1,ncases+1):
         row1 = int(next(lines)) - 1
         tab1 = [line_of_numbers(next(lines)) for i in range(4)]
         row2 = int(next(lines)) - 1
         tab2 = [line_of_numbers(next(lines)) for i in range(4)]
         result = process_case(row1, tab1, row2, tab2)
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
 
 ##start('A-test')
 start('A-small-attempt0')
 ##start('A-large')
