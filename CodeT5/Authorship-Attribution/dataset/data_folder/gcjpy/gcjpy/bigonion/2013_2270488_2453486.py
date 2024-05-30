directory = 'C:/users/hai/my projects/google code jam/2013/qualification/A/'
 
 
 def solve (f_in, f_out):
     N = int(f_in.readline())
     for testcase in range(1,N+1):
         sqr = []
         for i in range(4):
             sqr.append(list(f_in.readline().split()[0]))
         assert len(f_in.readline().split()) == 0
 
         f_out.write('Case #' + str(testcase) + ': ' + get_square_winner(sqr) +'\n')
     
 
 def get_all_lines(sqr):
     lines = []
     for line in sqr:
         lines.append(list(line))
     for column in range(4):
         line = []
         for row in range(4):
             line.append(sqr[row][column])
         lines.append(list(line))
 
     diag1 = []
     diag2 = []
     for  i in range(4):
         diag1.append(sqr[i][i])
         diag2.append(sqr[i][3-i])
     lines.append(diag1)
     lines.append(diag2)
 
     return lines
     
 def get_square_winner (sqr):
     for line in get_all_lines(sqr):
         if get_line_winner (line):
             return get_line_winner (line)
 
     for row in sqr:
         if '.' in row:
             return "Game has not completed"
     return "Draw"
 
 
 
 
 def get_line_winner (line):
     if line.count('X') == 4:
         return "X won"
     if line.count('X') == 3 and 'T' in line:
         return "X won"
     
     if line.count('O') == 4:
         return "O won"
     if line.count('O') == 3 and 'T' in line:
         return "O won"
 
 
     return None
 
 
 
 
 
 
 
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
