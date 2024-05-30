#
 # Google Code Jam 2012
 # Round 0: C. Recycled Numbers
 # submission by EnTerr
 #
 
 '''
 Limits: 1 <= T <= 50. A and B have the same number of digits.
 Small dataset: 1 <= A <= B <= 1000.
 Large dataset: 1 <= A <= B <= 2000000
 
 Input 
 4
 1 9
 10 40
 100 500
 1111 2222
  	
 Output 
 Case #1: 0
 Case #2: 3
 Case #3: 156
 Case #4: 287
 
 '''
 
 import psyco
 psyco.full()
 
 import sys
 from time import clock
 
 inf = open(sys.argv[1])
 def input(): return inf.readline().strip()
 
 def numRecycled(A,B):
     ln = len(str(A))
     rot = 10**(ln-1)
     cnt = 0
     for i in range(A,B+1):
         res = set()
         j = i
         for _ in range(ln-1):
             a,b = divmod(j, 10)
             j = rot*b + a
             if i < j <= B:
                 res.add(j)
         cnt += len(res)
     return cnt
 
 for caseNo in range(1, int(input())+1):
     #print >>sys.stderr, caseNo
     #tm = clock()
     print 'Case #%d:' % caseNo,
     A,B = map(int, input().split())
     print numRecycled(A,B)
     #print A, B, clock() - tm
 
