directory = 'C:/users/me/desktop/google code jam/2014/qualification/B/'
 
 
 
 def solve (f_in, f_out):
     T = int(f_in.readline())
     for testcase in range(1,T+1):
         line = f_in.readline()
         C,F,X = [float(q) for q in line.split()]
         result = compute (C,F,X)
         f_out.write('Case #' + str(testcase) + ': ' + str(result) + '\n')
 
 
 def compute(C,F,X):
     cps = 2
     farms = 0
     timespent = 0
     while X / cps > C/cps + X/(cps+F):
         farms += 1
         timespent += C/cps
         cps += F
 
     return timespent + X/cps
 
 
 
 
 
 def main_run():
     import os
     import time
     filenames = [x for x in os.listdir (directory)]
     filenames = [x for x in filenames if x.endswith('.in')]
     l1 = [(os.stat(directory+x).st_mtime, x) for x in filenames]
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
