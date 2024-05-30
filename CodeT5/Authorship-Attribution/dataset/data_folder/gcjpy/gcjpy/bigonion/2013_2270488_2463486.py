directory = 'C:/users/hai/my projects/google code jam/2013/qualification/C/'
 
 
 def is_palindrome (n):
     l = list(str(n))
     return list(reversed(l)) == l
 
 def prepare ():
     global fair_and_squares
     fair_and_squares = []
     
     for i in range(1,10**7):
         if is_palindrome(i):
             sqr = i**2
             if is_palindrome(sqr):
                 fair_and_squares.append(sqr)
     return
 
         
 def solve (f_in, f_out):
     prepare()
     T = int(f_in.readline())
     for testcase in range(1,T+1):
         A,B = [int(x) for x in f_in.readline().split()]
         count = len([x for x in fair_and_squares if (x>=A and x<=B)])
         f_out.write('Case #' + str(testcase) + ': ' + str(count) + '\n')
 
 
 
 def main_run():
     import os
     import time
     filenames = [x for x in os.listdir (directory)]
     filenames = [x for x in filenames if x.endswith('.in')]
     l1 = [(os.stat(directory+x).st_ctime, x) for x in filenames]
     chosen_filename =  sorted(l1)[-1][1][:-3]
 
     print ('Directory : ', directory)
     print ('Chosen Filename : ',chosen_filename)
     print()
     print ('Start : ', time.ctime())
     print()
     
     f_in = open(directory+chosen_filename+'.in')
     f_out = open(directory+chosen_filename+'.out', 'w')
     solve(f_in,f_out)
     f_in.close()
     f_out.close()
 
     print ()
     print ('End : ', time.ctime())
 
 
 main_run()
