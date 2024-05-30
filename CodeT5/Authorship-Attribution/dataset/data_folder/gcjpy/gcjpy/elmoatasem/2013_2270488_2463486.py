'''
 Created on Apr 12, 2013
 
 @author: Moatasem
 '''
 
 import math
 
 
 def isPalindrome(word):
     isPalin=False
     if(len(word)%2==0):
         f_half=word[0:len(word)/2];
         s_half=word[len(word)/2:len(word)][::-1]
         if( f_half==s_half):
             isPalin= True
     else:
         f_half=word[0:len(word)/2]
         s_half=word[(len(word)/2)+1:len(word)][::-1]
         if( f_half==s_half):
             isPalin= True
     return isPalin
     
 def getNumberOfFairAndSquare(range_):
     start=range_[0]
     end=range_[1]
     count_=0
     for i in range(start,end+1):
         root=math.sqrt(i);
         if(root.is_integer() and isPalindrome(str(int(root))) and isPalindrome(str(i))):
             count_+=1
     return count_
         
         
     
 
 f_r = open('C.in',"r")
 n_test=int(f_r.readline().strip()) 
 f_w = open("C.out", "w")
 for i in range(n_test):
     range_ =map(int,f_r.readline().split())
     result=getNumberOfFairAndSquare(range_)
     output_str='Case #{itr}: {res}'.format(itr=(i+1),res=result)
     f_w.write(output_str+'\n')
 f_r.close()
 f_w.close()