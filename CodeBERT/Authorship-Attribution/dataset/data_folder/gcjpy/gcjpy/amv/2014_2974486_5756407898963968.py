#!/usr/bin/env python
 import sys,os
 import numpy as np
 
 
 def Solve(F1,r1,F2,r2):
     s1=set(F1[r1-1])
     s2=set(F2[r2-1])
     sx=s1.intersection(s2)
     if len(sx)>1:
         return "Bad magician!"
     elif len(sx)==0:
         return "Volunteer cheated!"
     else:
         return sx.__iter__().next()
 
 
 
 def parse(infile):
     r1=int(infile.readline().strip())
     F1=[]
     for i in xrange(4):
         F1.append( map(int, infile.readline().split() ))
     r2=int(infile.readline().strip())
     F2=[]
     for i in xrange(4):
         F2.append( map(int, infile.readline().split() ))
     return F1,r1,F2,r2
 
 
 
 class GCJ_Parser( object ):
     def __init__(self,fname):
         self.infile=open(fname,'r')
         self.NumCases=int(self.infile.readline().strip() )
         self.caseNum=0
 
     def __iter__(self): return self
 
     def next(self):
         if self.caseNum==self.NumCases: raise StopIteration
         self.caseNum += 1
         args=parse(self.infile)
         return self.caseNum , args
 
 
 def runmain():
     myCases=GCJ_Parser(sys.argv[1])
 
     #Open output file, but don't overwrite old ones (for comparison)
     outname=sys.argv[1].rstrip('.in')+'.out'
     if os.path.isfile(outname):
         oldout=outname+'.old'
         ii=0
         while os.path.isfile(oldout):
             ii+=1
             oldout=outname+'.old'+str(ii)
         os.rename(outname,oldout)
         print 'Rename: %s -> %s'%(outname,oldout)   
  
     outfile=open(outname,'w')
 
     for iCase, args in myCases:
         answer=Solve(*args)
 
         print 'Case #'+str(iCase)+':',answer
         print >> outfile, 'Case #'+str(iCase)+':',answer
 
 
 
 
 if __name__=='__main__':
     runmain()
