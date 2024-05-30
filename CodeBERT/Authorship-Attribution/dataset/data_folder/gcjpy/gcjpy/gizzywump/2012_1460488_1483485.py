#!/usr/bin/env python
 
 import pdb
 import re
 import sys
 
 INPUT = "tiny"
 if 1:
     INPUT = "A-small-attempt2.in.txt"
 
 I=re.sub(" ", "", "ejp mysljylc kd kxveddknmc re jsicpdrysirbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcdde kr kd eoya kw aej tysr re ujdr lkgc jv")
 O=re.sub(" ", "", "our language is impossible to understandthere are twenty six factorial possibilitiesso it is okay if you want to just give up")
 
 #print I, O
 
 MAP={ 'z' : 'q', 'q' : 'z' }
 for i,o in zip(I,O):
     MAP[i] = o
 
 def debug(*args):
     pass #print str(args)
 
 def debug(*args):
     print str(args)
 
 def do_trial(l):
     t = list(l)
     t1 = [MAP.get(x, x) for x in t]
     return ''.join(t1)
 
 f = file(INPUT)
 T = int(f.readline()[:-1])
 for i in range(T):
     l = f.readline()[:-1]
     v = do_trial(l)
     print "Case #%d: %s" % (i+1, v)
