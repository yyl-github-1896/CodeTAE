#!/usr/bin/env python
 import sys,os
 import numpy as np
 import Queue
 
 #guaranteed that R,C>=3, and F is not 1,2,3,5,7
 def Fill(outmat,R,C,F):
     nF=F
     #first square
     outmat[:2,:2]='.'
     nF-=4
     if nF==0: return
 
     #next two
     outmat[2,:2]='.'
     nF-=2
     if nF==0: return    
 
     #nearly there...
     outmat[:2,2]='.'
     nF-=2
     if nF==0: return
 
     #Fill by 2 across columns
     for iC in xrange(3,C):
         if nF==1:
             outmat[2,2]='.'
             return
         outmat[:2,iC]='.'
         nF-=2
         if nF==0: return
         
     #Fill by 2 across rows
     for iR in xrange(3,R):
         if nF==1:
             outmat[2,2]='.'
             return
         outmat[iR,:2]='.'
         nF-=2
         if nF==0: return
 
     #Now fill singly 3rd row/column
     for iR,iC in ( (iR,iC) for iR in xrange(2,R)
                    for iC in xrange(2,C)):
         outmat[iR,iC]='.'
         nF-=1
         if nF==0: return
     
 
 
 
 def Solve(R,C,M):
     F=R*C-M
     if F==0: return '\nImpossible'
     if (R>1 and C>1 and F in (2,3)):
         return '\nImpossible'
 
     outmat=np.zeros( (R,C), dtype='S1')
     outmat[:,:]='*'
 
     if R==1:
         for i in xrange(F):
             outmat[0][i]='.'
     
     elif C==1:
         for i in xrange(F):
             outmat[i][0]='.'
 
     elif F>1:
         if F in (2,3,5,7): return "\nImpossible"
         elif (R==2 or C==2) and F%2 != 0:
             return "\nImpossible"
         elif R==2:
             outmat[:,:F/2]='.'
         elif C==2:
             outmat[:F/2,:]='.'
         else: Fill(outmat,R,C,F)
         
     outmat[0,0]='c'
     outmatlines=[ ''.join(x) for x in outmat ]
     #print outmatlines
     answer='\n'+'\n'.join(outmatlines)
 
     Verify(answer,F)
 
     return answer
 
 disp=[ (dx,dy) for dx in (-1,0,1)
     for dy in (1,0,-1) if (dx !=0 or dy!=0) ]
 
 def Verify(answer,F):
     lines=[list(x) for x in answer.split('\n')]
     if len(lines[0])==0: lines.pop(0)
     R,C=len(lines),len(lines[0])
     assert lines[0][0]=='c'
     assert answer.count('.')+1==F
     q=Queue.Queue()
     q.put( (0,0) )
 
     def adjToMine(x,y):
         for dx,dy in disp:
             if 0<=x+dx<R and 0<=y+dy<C:
                 if lines[x+dx][y+dy]=='*': return True
         return False
                 
 
     while not q.empty():
         x,y=q.get()
         for dx,dy in disp:
             if 0<=x+dx<R and 0<=y+dy<C:
                 if lines[x+dx][y+dy]=='c': continue
                 lines[x+dx][y+dy]='c'
                 if not adjToMine(x+dx,y+dy):
                     q.put( (x+dx,y+dy) )
 
     clicked='\n'.join([ ''.join(x) for x in lines])
     if clicked.find('.')>=0:
         print '\n','*'*20,"\nERROR, input:"
         print answer
         print 'OUTPUT:'
         print clicked
     
 
 
 
 def parse(infile):
     R,C,M=map(int, infile.readline().split() )
     return R,C,M
 
 
 
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
