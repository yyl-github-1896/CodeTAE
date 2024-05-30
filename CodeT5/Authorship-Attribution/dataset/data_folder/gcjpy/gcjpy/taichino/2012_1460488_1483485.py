#!/usr/bin/python
 # -*- coding: utf-8 -*-
 
 import sys
 
 alphabet = 'abcdefghijklmnopqrstuvwxyz'
 gog = 'ejp mysljylc kd kxveddknmc re jsicpdrysi' + \
       'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd' + \
       'de kr kd eoya kw aej tysr re ujdr lkgc jv' + \
       'y qee'
 
 eng = 'our language is impossible to understand' + \
       'there are twenty six factorial possibilities' + \
       'so it is okay if you want to just give up' + \
       'a zoo'
 
 rule = {}
 for i, c in enumerate(gog):
    rule[c] = eng[i]
 
 gog_alphabet = rule.keys()
 eng_alphabet = rule.values()
 missing_key = None
 missing_val = None
 for c in alphabet:
     if not c in gog_alphabet:
         missing_key = c
     if not c in eng_alphabet:
         missing_val = c
 rule[missing_key] = missing_val
 
 for i, line in enumerate(sys.stdin):
     if i == 0:
         continue
 
     orig = line.strip()
     ans = ''.join([rule[c] for c in orig])
     print 'Case #%(i)s: %(ans)s' % locals()
 
