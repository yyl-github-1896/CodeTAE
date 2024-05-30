#
 # Google Code Jam 2013
 # Round 0: B. Lawnmower
 # submission by EnTerr
 #
 
 '''
 Limits
 
 1 <= T <= 100.
 
 Small dataset   1 <= N, M <= 10. 1 <= a[i,j] <= 2.
 Large dataset   1 <= N, M <= 100. 1 <= a[i,j] <= 100.
 
 Sample
 
 *** Input 
 3
 3 3
 2 1 2
 1 1 1
 2 1 2
 5 5
 2 2 2 2 2
 2 1 1 1 2
 2 1 2 1 2
 2 1 1 1 2
 2 2 2 2 2
 1 3
 1 2 1
 
 *** Output 
 Case #1: YES
 Case #2: NO
 Case #3: YES
 
 '''
 
 #import psyco
 #psyco.full()
 
 import sys
 from time import clock
 
 inf = open(sys.argv[1])
 def input(): return inf.readline().strip()
 
 
 def check_lawn(board):
     n = len(board)
     m = len(board[0])
     hmax = map(max, board)
     vmax = map(max, zip(*board))
     for i in range(n):
         for j in range(m):
             if board[i][j] < min(hmax[i], vmax[j]):
                 return 'NO'
     return 'YES'
 
 for caseNo in range(1, int(input())+1):
     #tm = clock()
     n,m = map(int, input().split())
     board = [map(int, input().split()) for _ in range(n)]
     print 'Case #%d:' % caseNo, check_lawn(board)
     #print >>sys.stderr, caseNo, clock() - tm
 
