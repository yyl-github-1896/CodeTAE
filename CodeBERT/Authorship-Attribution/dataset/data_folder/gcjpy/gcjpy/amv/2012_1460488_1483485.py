#!/usr/bin/env python
 import sys
 import numpy as np
 
 infile=open(sys.argv[1],'r')
 
 NumCases=int(infile.readline())
 
 myinput="""ejp mysljylc kd kxveddknmc re jsicpdrysi
 rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
 de kr kd eoya kw aej tysr re ujdr lkgc jv"""
 
 myoutput=\
 """our language is impossible to understand
 there are twenty six factorial possibilities
 so it is okay if you want to just give up"""
 
 mapping={}
 mapping['q']='z'
 mapping['z']='q'
 
 
 for char,mapto in zip(myinput,myoutput):
     if mapping.has_key(char):
         assert mapping[char]==mapto
     else:
         mapping[char]=mapto
 
 #allchar=set('abcdefghijklmnopqrstuvwxyz')
 #print allchar-set( mapping.keys() )
 #print allchar-set(mapping.values() )
 
 
 
 for iCase in xrange(NumCases):
     thestring=infile.readline().strip()
 
     newstring=''
     for char in thestring: newstring+=mapping[char]
 
 
     print 'Case #'+str(iCase+1)+': '+newstring
 
