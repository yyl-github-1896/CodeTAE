#!/usr/bin/env python
 import sys
 import numpy as np
 
 
 def Solve(n,m,heights):
     #print heights
     for i,j in ( (i,j) for i in xrange(n) for j in xrange(m) ):
         if (heights[i,:]<= heights[i,j]).all(): continue
 
         if (heights[:,j]>heights[i,j]).any(): return "NO"
 
 
     return 'YES'
 
 
 
 def parse(infile):
     n,m=map(int, infile.readline().split() )
     heights=np.zeros( (n,m) )
     for i in xrange(n):
         heights[i,:]=np.array( map(int, infile.readline().split() ) )
     return n,m,heights
 
 
 
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
     outfile=open(sys.argv[1].rstrip('.in')+'.out','w')
 
     for iCase, args in myCases:
         answer=Solve(*args)
 
         print 'Case #'+str(iCase)+':',answer
         print >> outfile, 'Case #'+str(iCase)+':',answer
 
 
 
 
 ########library functions
 class Categorizer(dict):
     def __init__(self,thelist,transform,trunc=2):
         dict.__init__(self)
         self.transform=transform
         self.AddList(thelist)
         self.trunc=trunc
     def AddList(self,thelist):
         for item in thelist: self.Add( item )
     def Add(self,object):
         cat=self.transform( object )
         if type(cat) is float:
             cat=round(cat,trunc)
         if self.has_key(cat):
             self[cat].append( object )
         else:
             self[cat]=[object]
     def PrintRanking(self,n=None):
         if n is None: n=len(self)
         items=self.items()
         items.sort(key=lambda x:-len(x[1]))
         total=0
         for i in items: total+=len(i[1])
         maxkey=max( len(str(key)) for key in self.iterkeys() )
         maxval=max( len(str(len(val))) for val in self.itervalues() )
         formatter="{0:<"+str(maxkey)+"} {1:>"+str(maxval)+"}    {2}"
         for key,count in items[0:n]:
             print formatter.format(key,len(count),
                                    ("%.2f"%(len(count)*100.0/total))+'%')
     def Combine(self,newdict):
         newkeys=newdict.keys()
         for key in newkeys:
            if not type(newdict[key])==int:
               raise TypeError('passed object is not a counter')
         for key in newkeys:
            if not self.has_key(key): self[key]=[]
            self[key] += newdict[key]
     def Avg(self):
         avg=0.0
         ntot=0
         for key in self.keys():
             ntot+=len(self[key])
             avg+=len(self[key])*key
         return avg/(1.0*ntot)
     def StdDev(self):
         avg=self.Avg()
         ntot=0
         stddev=0.0
         for key in self.iterkeys():
             ntot+=len(self[key])
             stddev += len(self[key]) * ( (key-avg)**2)
         return stddev/(1.0*ntot)
     def Median(self):
         tot=0
         for value in self.itervalues(): tot+=len(value)
         keys=self.keys()
         keys.sort()
         nCount=0
         for key in keys:
            nCount += len(self[key])
            if nCount>tot/2: return key
     def Mode(self):
         return max(self.iteritems(), key=lambda x: len(x[1]))[0]
 
 
 
 
 class Counter(dict):
     def __init__(self,thelist,transform=None,trunc=2):
         dict.__init__(self)
         self.transform=transform
         self.trunc=trunc
         self.AddList(thelist)
     def AddList(self,thelist):
         if self.transform is not None:
             for item in thelist: self.Add( self.transform(item) )
         else:
             for item in thelist: self.Add( item )            
     def Add(self,object):
         if type(object) is float:
             object=round(object,self.trunc)
         if self.has_key(object):
             self[object]+=1
         else:
             self[object]=1
     def PrintRanking(self,n=None):
         if n is None: n=len(self)
         items=self.items()
         items.sort(key=lambda x:-x[1])
         total=0
         for i in items: total+=i[1]
         maxkey=max( len(str(key)) for key in self.iterkeys() )
         maxval=max( len(str(val)) for val in self.itervalues() )
         formatter="{0:<"+str(maxkey)+"} {1:>"+str(maxval)+"}    {2}"
         for key,count in items[0:n]:
             print formatter.format(key,count, ("%.2f"%(count*100.0/total))+'%')
     def Combine(self,newdict):
         newkeys=newdict.keys()
         for key in newkeys:
            if not type(newdict[key])==int:
               raise TypeError('passed object is not a counter')
         for key in newkeys:
            if not self.has_key(key): self[key]=0
            self[key] += newdict[key]
     def Avg(self):
         avg=0.0
         ntot=0
         for key in self.keys():
             ntot+=self[key]
             avg+=self[key]*key
         return avg/(1.0*ntot)
     def StdDev(self):
         avg=self.Avg()
         ntot=0
         stddev=0.0
         for key in self.iterkeys():
             ntot+=self[key]
             stddev += self[key] * ( (key-avg)**2)
         return stddev/(1.0*ntot)
     def Median(self):
  	total=sum(self.values())
         keys=self.keys()
         keys.sort()
         nCount=0
         for key in keys:
            nCount += self[key]
            if nCount>total/2: return key
     def Mode(self):
         return max(self.iteritems(), key=lambda x: x[1])[0]
 
 
 def gen_primes():
     """ Generate an infinite sequence of prime numbers.
     from http://stackoverflow.com/questions/1628949/to-find-first-n-prime-numbers-in-python
     """
     D = {}  
     q = 2  
 
     while True:
         if q not in D:
             yield q        
             D[q * q] = [q]
         else:
             for p in D[q]:
                 D.setdefault(p + q, []).append(p)
             del D[q]
 
         q += 1
 
 
 
 if __name__=='__main__':
     runmain()
