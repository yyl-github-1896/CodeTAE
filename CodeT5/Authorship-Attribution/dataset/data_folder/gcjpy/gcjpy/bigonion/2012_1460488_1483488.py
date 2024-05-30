directory = 'C:/users/hai/my projects/google code jam/2012/qualification/C/'
 
 
 def solve (f_in, f_out):
     pre_calc = prepare()
     T = int(f_in.readline())
     for i in range(1,T+1):
         A,B = [int(x) for x in f_in.readline().split()]
         c = 0
         for m in range(A,B+1):
             c += len ([n for n in pre_calc[m] if n >=A])
         f_out.write('Case #' + str(i) + ': ' + str(c) + '\n')
 
 
 
 
 
 
 def prepare ():
     l = [None]* 2000001
     for n in range(1,2000001):
         recycled = []
         s = str(n)
         for c in range(1, len(s)):
             s2 = s[c:] + s[:c]
             if s2[0] != '0':
                 n2 = int(s2)
                 if n2 < n and n2 not in recycled:
                     recycled.append(n2)
         #recycled.sort()
         l [n] = recycled
     return l
 
 
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
