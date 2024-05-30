#!/usr/bin/env python
 
 
 _inp = (
     'ejp mysljylc kd kxveddknmc re jsicpdrysi',
     'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd',
     'de kr kd eoya kw aej tysr re ujdr lkgc jv',
 )
 
 _out = (
     'our language is impossible to understand',
     'there are twenty six factorial possibilities',
     'so it is okay if you want to just give up',
 )
 
 def compute_lang_map(inp, out):
     lang_map = {}
     for gs, ss in zip(inp, out):
         for gl, sl in zip(gs, ss):
             lang_map[gl] = sl
     lang_map['q'] = 'z'
     lang_map['z'] = 'q'
     return lang_map
 
 _lang_map = compute_lang_map(_inp, _out)
 def conv(s):
     out = ''
     for l in s:
         out += _lang_map[l]
     return out
 
 def main():
     with open('input-file', 'r') as f:
         f.readline()            # skip T
         n = 0
         for line in f:
             n += 1
             print 'Case #%d: %s' % (n, conv(line.strip()))
 
 if __name__ == '__main__':
     main()
