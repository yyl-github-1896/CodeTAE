directory = 'C:/users/hai/my projects/google code jam/2013/qualification/B/'
 
 
 from copy import deepcopy
 
 def solve (f_in, f_out):
     T = int(f_in.readline())
     for testcase in range(1,T+1):
         print (testcase)
         N,M = [int(x) for x in f_in.readline().split()]
         sqr = []
         for i in range(N):
             sqr.append([int(x) for x in f_in.readline().split()])
         res = get_result(sqr)
         f_out.write('Case #' + str(testcase) + ': ' + res + '\n')
 
 
 def get_result (sqr):
     while len(sqr) > 1 and len(sqr[0]) > 1:
         print (sqr)
         r,c = 0,0
         for row in range(len(sqr)):
             for col in range(len(sqr[0])):
                 if sqr[row][col] < sqr[r][c]:
                     r,c = row, col
         min_val = sqr[r][c]
         whole_row = list(sqr[r])
         whole_col = []
         for row in range(len(sqr)):
             whole_col.append(sqr[row][c])
         assert min(whole_row) == min_val
         assert min(whole_col) == min_val
         if max(whole_row) == min_val:
             sqr = remove_row(sqr,r)
         elif max(whole_col) == min_val:
             sqr = remove_col(sqr,c)
         else:
             return 'NO'
 
     return 'YES'
     
 
 
 
 
 
 def remove_row (sqr, row):
     cpy = deepcopy(sqr)
     del cpy[row]
     return cpy
 
 def remove_col (sqr,col):
     cpy = deepcopy(sqr)
     for row in cpy:
         del row[col]
     return cpy
 
 
 
 
 
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
