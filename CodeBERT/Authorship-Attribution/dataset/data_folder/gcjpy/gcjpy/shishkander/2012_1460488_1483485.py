#!/usr/bin/env python
 
 IN = """
 ejp mysljylc kd kxveddknmc re jsicpdrysi
 rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
 de kr kd eoya kw aej tysr re ujdr lkgc jv"""
 OUT ="""
 Case #1: our language is impossible to understand
 Case #2: there are twenty six factorial possibilities
 Case #3: so it is okay if you want to just give up"""
 
 ins = IN.strip().split("\n")
 outs = OUT.strip().split("\n")
 assert len(ins) == len(outs) == 3
 
 D = {}
 D['a'] = 'y'
 D['o'] = 'e'
 D['z'] = 'q'
 
 for case, s in enumerate(ins):
     out = outs[case][9:] # skip "Case #?: "
     assert len(out) == len(s)
     for i, o in enumerate(out):
         if o == ' ': continue
         D[s[i]] = o
 
 if len(D) == 25:
     chars = map(chr, xrange(97, 123))
     key = set(chars).difference( set(D.keys()) ).pop()
     value = set(chars).difference( set(D.values()) ).pop()
     D[key] = value
 assert len(D) == 26
 D[' '] = ' '
 
 
 def solve(fin, fout):
     T = int(fin.readline())
     for t in xrange(T):
         fout.write("Case #%i: " % (t+1) )
         for c in fin.readline().strip():
             fout.write(D[c])
         fout.write('\n')
     return True
 
 if __name__ == "__main__":
     import sys
     with open(sys.argv[1],'r') as fin:
         with open(sys.argv[2], 'w') as fout:
             solve(fin, fout)
