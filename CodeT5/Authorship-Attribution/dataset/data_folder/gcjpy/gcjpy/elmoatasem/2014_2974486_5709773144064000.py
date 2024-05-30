'''
 Created on Apr 11, 2014
 
 @author: mostasem
 '''
 
 
 def getSeconds(C,F,X):
     seconds = 0.0
     cookie_rate = 2
     solved =False
     while (not solved):
         choice1 = X/cookie_rate
         choice2 = C/cookie_rate + X/(cookie_rate + F)
         if(choice1 < choice2):
             seconds += choice1
             solved = True
         else :
             seconds += C/cookie_rate
             cookie_rate += F
     
     return seconds
 
 f_r = open('B.in',"r")
 n_test=int(f_r.readline().strip()) 
 f_w = open("B.out", "w")
 result = ""
 for i in range(n_test):
     C,F,X = map(float,f_r.readline().split())
     seconds = getSeconds(C,F,X)
     result = str(seconds)
     output_str='Case #{itr}: {res}'.format(itr=(i+1),res=result)
     f_w.write(output_str+'\n')
     
 f_r.close()
 f_w.close()
 
