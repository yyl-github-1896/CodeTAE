'''
 Created on Apr 14, 2012
 
 @author: moatasem
 '''
 
 
 def isSurprising(t):
     if(abs(t[0]-t[1])==2 or abs(t[2]-t[1])==2 or abs(t[0]-t[2])==2):
         return True
     else:
         return False
 
 
 def getAllTriplets(n):
     h=[]
     for i in xrange(11):
         for j in xrange(i,11):
             for  k in xrange(j,11):
                 if(i+j+k==n and abs(i-j)<3 and abs(k-j)<3 and abs(i-k)<3):
                     h.append((i,j,k))
             
     return  h
 
 def getInfo(p,total,S):
     g= getAllTriplets(total)
     #print total
     #print g
     if(S):
         s_=len(g)
         indcies=[]
         for i in xrange (s_):
             if(isSurprising(g[i])):
                 indcies.append(i)
         for i in xrange (len(indcies)):  
             g.remove(g[indcies[i]])
     #print g
     equ=False
     sur=False
     sur_equ=False
     for i in xrange(len(g)):
         if(max(g[i])>=p):
             if(isSurprising(g[i])):
                 #print g[i]
                 sur_equ=True
             else:
                 equ=True
         elif(isSurprising(g[i])):
                 sur=True
     return sur_equ,equ,sur
            
 f = open("b_.in", "r")
 n=int(f.readline().strip())
 for k  in xrange(n):
     d=f.readline().strip()
     googlers=[]
     g=[int(i) for i in d.split(" ")]
     N=g[0]
     S=g[1]
     noSu=False
     if(S==0):
         noSu=True
     p=g[2]
     count=0
     equ_count=0;
     both_count=0;
     sur_count=0;
     first_count=0;
     googlers=g[3:len(g)]
     for o in xrange(N):
         info=getInfo(p,googlers[o],noSu)
         #print info
         if(info[0]==True and info[1]==False and S<>0): #101 /100
             count+=1
             S-=1
         elif(info[0]==True and info[1]==True):#110 / 111
             first_count+=1
         elif(info[1]==True and info[2]==True):#011
             both_count+=1
         elif(info[1]==True):#010
             count+=1
         elif(info[2]==True):#001
             sur_count+=1
     count+=first_count
     if(S>0):
         if(first_count>S):
             S=0
         elif(first_count <=S) :
             S-=first_count
             if(S>0):
                  if(both_count>S):
                     both_count-=S
                     S=0
                  else:
                     both_count=0
     count+=both_count
     
     print 'Case #'+str((k+1))+": "+str(count)
 
 
 
 
 
 
 
 
 
 
     
 
 #f=getAllTriplets(18)
 #print f
 #for i in xrange(len(f)):
 #    print isSurprising(f[i])