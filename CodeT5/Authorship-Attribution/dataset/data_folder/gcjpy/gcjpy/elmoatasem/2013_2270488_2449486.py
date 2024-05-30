'''
 Created on Apr 12, 2013
 
 @author: Moatasem
 '''
 
 import math
 
 
 
 
 def markMax(max_,start,end,marked,isRow,lawn):
     for i in range(end):
             if(isRow):
                 if( lawn[start][i]==max_):
                     marked[start][i]=-1
             else: 
                 if( lawn[i][start]==max_):
                     marked[i][start]=-1
                     
                 
     
     
 def mowerLawn(lawn,m,n,marked):
     #marked= [[0] *n]*m
     for i in range(m):
         max_=max(lawn[i])
         markMax(max_,i,n,marked,True,lawn) 
     
     for i in range(n):
         colList=[]
         for j in range(m):
             colList.append(lawn[j][i])
         max_=max(colList)
         markMax(max_,i,m,marked,False,lawn) 
            
     done=True
     for i in range(m):
         for j in range(n):
             if(marked[i][j]!=-1):
                 done=False
                 break
         if(not done):
             break
     if(done):
         return 'YES'
     else:
         return 'NO'
     
         
     
 
 f_r = open('B.in',"r")
 n_test=int(f_r.readline().strip()) 
 f_w = open("B.out", "w")
 for i in range(n_test):
     lawn=[]
     
     range_ =map(int,f_r.readline().split())
     #marked= [[0] *range_[1]]*range_[0]
     marked=[[0]*range_[1] for x in xrange(range_[0])]
     for j in range(range_[0]):
         temp=[map(int,f_r.readline().split())]
         lawn.extend(temp)
     result=mowerLawn(lawn,range_[0],range_[1],marked)
     output_str='Case #{itr}: {res}'.format(itr=(i+1),res=result)
     f_w.write(output_str+'\n')
 f_r.close()
 f_w.close()