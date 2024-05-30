#!/usr/bin/env python
 import sys
 import numpy as np
 
 infile=open(sys.argv[1],'r')
 
 NumCases=int(infile.readline())
 
 for iCase in xrange(NumCases):
 
     a,b=[int(i) for i in infile.readline().split()]
 
 
 #for iCase in xrange(1):
 #    a,b=[int(i) for i in sys.argv[1:]]
     a_digits=[int(i) for i in str(a) ]
     b_digits=[int(i) for i in str(b) ]
 
     ld=len(a_digits)
 
 #    print a_digits,b_digits
 
     result=0
 #    lowers={}
 
     for iNum in xrange(a,b+1):
         mystr=str(iNum)
         myset=set()
         for i in xrange(1,ld):
             mystr=mystr[1:]+mystr[0]
             iii=int(mystr)
             if iii>iNum and iii<=b and iii not in myset:
                 result+=1
                 #print iNum,iii
                 #if lowers.has_key(iii):
                 #    lowers[iii].append(iNum)
                 #else: lowers[iii]=[iNum]
 
             myset.add(iii)
             
         
 
 
 #    for k,v in lowers.iteritems(): print k,':',v
     print 'Case #'+str(iCase+1)+':',result
 
