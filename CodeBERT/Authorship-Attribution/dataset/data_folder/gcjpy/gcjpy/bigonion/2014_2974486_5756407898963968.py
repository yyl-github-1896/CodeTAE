directory = 'C:/users/me/desktop/google code jam/2014/qualification/A/'
 
 
 
 def solve (f_in, f_out):
     T = int(f_in.readline())
     for testcase in range(1,T+1):
         
         c1 = int(f_in.readline())
         l1 = []
         for i in range(4):
             l1.append(f_in.readline())
         
         c2 = int(f_in.readline())
         l2 = []
         for i in range(4):
             l2.append(f_in.readline())
 
         d1 = l1[c1-1].split()
         d2 = l2[c2-1].split()
 
         foundFlag = False
         chosenCard = None
         badMagician = False
         for card in d1:
             if card in d2:
                 if not foundFlag:
                     foundFlag = True
                     chosenCard = card
                 else:
                     badMagician = True
 
         f_out.write('Case #' + str(testcase) + ': ')
         if badMagician:
             f_out.write('Bad magician!\n')
         elif not foundFlag:
             f_out.write('Volunteer cheated!\n')
         else:
             f_out.write(chosenCard + '\n')
 
 
 
 
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
