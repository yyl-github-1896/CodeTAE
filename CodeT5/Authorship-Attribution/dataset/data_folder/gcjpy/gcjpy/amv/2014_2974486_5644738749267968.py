#!/usr/bin/env python
 import sys,os
 import numpy as np
 
 
 def Solve(N,n,k):
     n.sort(reverse=True)
     k.sort(reverse=True)
     nDW=0
     i_n,i_k=0,0
     while i_n<N and i_k<N:
         if n[i_n]>k[i_k]:
             nDW+=1
             i_n+=1
             i_k+=1
         else:
             i_k+=1
 
     nW=0
     i_n,i_k=0,0
     while i_n<N and i_k<N:
         if n[i_n]<k[i_k]:
             nW+=1
             i_n+=1
             i_k+=1
         else:
             i_n+=1
 
     nW=N-nW
     return '%d %d'%(nDW,nW)
 
 
 
 def parse(infile):
     N=int(infile.readline().strip())
     n=map(float, infile.readline().split() )
     k=map(float, infile.readline().split() )
     return N,n,k
 
 
 
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
