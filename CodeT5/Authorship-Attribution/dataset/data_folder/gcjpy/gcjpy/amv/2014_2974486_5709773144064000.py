#!/usr/bin/env python
 import sys,os
 import numpy as np
 
 BIG_NUM=100000
 def Solve(C,F,X):
     best_time=float('inf')
     for n in xrange(0,BIG_NUM):
         if n==0:
             farm_time=0
         else:
             farm_time += C/(2+(n-1)*F)
         if best_time<=farm_time: break
         cookie_time=X/(2+n*F)
 
         if farm_time+cookie_time<best_time:
             best_time=farm_time+cookie_time
 
     return '%.9f'%best_time
 
 
 
 def parse(infile):
     C,F,X=map(float, infile.readline().split() )
     return C,F,X
 
 
 
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
