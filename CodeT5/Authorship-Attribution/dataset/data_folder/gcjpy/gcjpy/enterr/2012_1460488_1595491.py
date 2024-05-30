#
 # Google Code Jam 2012
 # Round 0: B. Dancing With the Googlers
 # submission by EnTerr
 #
 
 '''
 Limits: T in [1,100], S in [0,N], p in [0,10], Ti in [0, 30]
 At least S of the ti values will be between 2 and 28, inclusive.
 
 Small dataset 1 = N = 3.
 Large dataset 1 = N = 100.
 
 Sample Input 
 4
 3 1 5 15 13 11
 3 0 8 23 22 21
 2 1 1 8 0
 6 2 8 29 20 8 18 18 21
 
 Output 
 Case #1: 3
 Case #2: 2
 Case #3: 1
 Case #4: 3
 '''
 
 #import psyco
 #psyco.full()
 
 import sys
 from time import clock
 
 inf = open(sys.argv[1])
 def input(): return inf.readline().strip()
 
 def maxBestDancers(N, S, p, *Ti):
     cnt = 0
     for score in Ti:
         mx = (score + 2) // 3
         if mx >= p:
             cnt += 1
         elif mx >= p-1 > 0 and S>0:
             S -= 1
             cnt += 1
     return cnt
 
 for caseNo in range(1, int(input())+1):
     #tm = clock()
     print 'Case #%d:' % caseNo,
     lst = map(int, input().split())
     print maxBestDancers(*lst)
     #print >>sys.stderr, caseNo, clock() - tm
 
