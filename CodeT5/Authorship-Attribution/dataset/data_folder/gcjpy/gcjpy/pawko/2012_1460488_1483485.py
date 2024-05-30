# python 3
 import string
 import itertools
 import sys
 
 samples = [('a zoo',
             'y qee'),
            ('our language is impossible to understand',
             'ejp mysljylc kd kxveddknmc re jsicpdrysi'),
            ('there are twenty six factorial possibilities',
             'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd'),
            ('so it is okay if you want to just give up',
             'de kr kd eoya kw aej tysr re ujdr lkgc jv')]
            
 def process_case(line, trans):
     return ''.join(trans[ch] for ch in line)
 
 def prepare_translation():
     trans = {}
     for eg_seqs in samples:
         for echar,gchar in zip(*eg_seqs):
             trans[gchar] = echar
     miss_g = set(string.ascii_lowercase) - set(trans.keys())
     miss_e = set(string.ascii_lowercase) - set(trans.values())
     if (len(miss_g) == 1 and len(miss_e) == 1):
         trans[miss_g.pop()] = miss_e.pop();
     return trans
 
 def result_gen(lines):
     trans = prepare_translation()
     ncases = int(next(lines))
     for ci in range(1,ncases+1):
         result = process_case(next(lines), trans)
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
