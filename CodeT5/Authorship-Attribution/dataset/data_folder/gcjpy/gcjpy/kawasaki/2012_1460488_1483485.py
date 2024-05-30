# -*- coding: utf-8 -*-
 
 import string
 
 
 str_to = '''
 ejp mysljylc kd kxveddknmc re jsicpdrysi
 rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
 de kr kd eoya kw aej tysr re ujdr lkgc jv
 '''.replace(' ', '').replace('\n', '')
 
 str_from = '''
 our language is impossible to understand
 there are twenty six factorial possibilities
 so it is okay if you want to just give up
 '''.replace(' ', '').replace('\n', '')
 
 conv = {}
 for i, c in enumerate(str_from):
     assert c not in conv or conv[c] == str_to[i]
     conv[c] = str_to[i]
 conv['z'] = 'q'
 conv['q'] = 'z'
 
 assert len(set(conv.keys())) == 26
 assert len(set(conv.values())) == 26
 mat = ['', '']
 for k, v in conv.items():
     mat[0] += v
     mat[1] += k
 
 T = int(raw_input())
 for case in xrange(1, T + 1):
     line = raw_input()
     ans = string.translate(line, string.maketrans(*mat))
     print 'Case #%d: %s' % (case, ans)
 
