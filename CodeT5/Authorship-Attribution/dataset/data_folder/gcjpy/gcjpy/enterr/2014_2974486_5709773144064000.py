#
 # Google Code Jam 2014
 # Roaund 0: B. Cookie Clicker Alpha
 # submission by EnTerr
 #
 
 '''
 Input
 The first line of the input gives the number of test cases, T. T lines follow. 
 Each line contains three space-separated real-valued numbers: C, F and X.
 
 Output
 For each test case, output one line containing "Case #x: y", where x is 
 the test case number (starting from 1) and y is the minimum number of seconds 
 it takes before you can have X delicious cookies.
 
 We recommend outputting y to 7 decimal places, but it is not required. 
 y will be considered correct if it is close enough to the correct number: 
 within an absolute or relative error of 10^-6. 
 
 Limits
 1 <= T <= 100.
 
 Small dataset
 1 <= C <= 500.
 1 <= F <= 4.
 1 <= X <= 2000.
 
 Large dataset
 1 <= C <= 10000.
 1 <= F <= 100.
 1 <= X <= 100000.
 
 
 ---Input  
 4
 30.0 1.0 2.0
 30.0 2.0 100.0
 30.50000 3.14159 1999.19990
 500.0 4.0 2000.0
 
 ---Output 
 Case #1: 1.0000000
 Case #2: 39.1666667
 Case #3: 63.9680013
 Case #4: 526.1904762
 
 '''
 
 
 
 import sys
 from time import clock
 
 
 f = open(sys.argv[1])
 def input(): return f.readline().strip();
 
 def bestTime(C, F, X):
     #C= cost of cookie farm, ck
     #F= farm production, ck/sec
     #X= goal, ck
     v = 2   #speed of production, cookies/sec
     t = 0   #total time of production, sec
     while True:
         tX = X / v          #time to reach goal at current speed
         tC = C / v          #time to buy farm
         tXc = X / (v + F)   #time to reach goal after adding farm
         if tX <= tC + tXc:
             #no more farms
             break
         #we are buying farm
         t += tC
         v += F
     #finishing at current speed
     t += tX
     return t
 
 #clk = clock()
 
 for caseNo in xrange(1, int(input())+1):
     C, F, X = map(float, input().split())
     #print >>sys.stderr, caseNo
     print 'Case #%d: %.7f' % (caseNo, bestTime(C, F, X))
     
 #print >>sys.stderr, 'time= %.1f seconds' % (clock()-clk )
 
 
