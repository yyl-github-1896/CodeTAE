#
 # Google Code Jam 2014
 # Roaund 0: D. Deceitful War
 # submission by EnTerr
 #
 
 '''
 Input
 The first line of the input gives the number of test cases, T. T test cases follow. 
 Each test case starts with a line containing a single integer N, the number of blocks 
 each player has. Next follows a line containing N space-separated real numbers: 
 the masses of Naomi's blocks, in kg. Finally there will be a line containing N 
 space-separated real numbers: the masses of Ken's blocks, in kg.
 
 Output
 For each test case, output one line containing "Case #x: y z", where 
 x is the test case number (starting from 1), 
 y is the number of points Naomi will score if she plays Deceitful War optimally, and 
 z is the number of points Naomi will score if she plays War optimally.
 
 Limits
 1 <= T <= 50.
 All the masses given to Ken and Naomi are distinct, and between 0.0 and 1.0 exclusive.
 
 Small dataset
 1 <= N <= 10.
 
 Large dataset
 1 <= N <= 1000.
 
 ---Input 
 4
 1
 0.5
 0.6
 2
 0.7 0.2
 0.8 0.3
 3
 0.5 0.1 0.9
 0.6 0.4 0.3
 9
 0.186 0.389 0.907 0.832 0.959 0.557 0.300 0.992 0.899
 0.916 0.728 0.271 0.520 0.700 0.521 0.215 0.341 0.458
 
 ---Output 
 Case #1: 0 0
 Case #2: 1 0
 Case #3: 2 1
 Case #4: 8 4
 
 
 '''
 
 import sys
 from time import clock
 
 f = open(sys.argv[1])
 def input(): return f.readline().strip();
 
 
 
 def deceitfulWar(Naomi, Ken):
     Naomi = Naomi[:]
     Ken = Ken[:]
     pts = 0
     while Naomi and Ken and Naomi[-1] > Ken[0]:
         #Naomi's max is bigger than Ken's min
         #lie to force him to throw out the min
         #fore-"trump" with smallest bigger card
         kn = Ken.pop(0)
         for i in range(len(Naomi)):
             if Naomi[i] > kn:
                 #since Naomi[-1] > kn, we'll get here
                 Naomi.pop(i)
                 break
         pts += 1        
 
     return pts
 
 def war(Naomi, Ken):
     Naomi = Naomi[:]
     Ken = Ken[:]
     pts = 0
     while Naomi and Ken:
         #naomi plays her smallest
         nm = Naomi.pop(0)
         if nm > Ken[-1]:
             #if Ken cannot beat, he plays his smallest
             Ken.pop(0)
             pts += 1
         else:
             #if he can beat, he finds the smallest above nm
             for i in range(len(Ken)):
                 if Ken[i] > nm:
                     #since Ken[-1] > nm, we'll get here
                     Ken.pop(i)
                     break          
     return pts
 
 #clk = clock()
 
 for caseNo in xrange(1, int(input())+1):
     #print >>sys.stderr, caseNo
     _ = input()
     Naomi = sorted(map(float, input().split()))
     Ken = sorted(map(float, input().split()))
     print 'Case #%d:' % caseNo, deceitfulWar(Naomi, Ken), war(Naomi, Ken)
     
 #print >>sys.stderr, 'time= %.1f seconds' % (clock()-clk )
 
 
