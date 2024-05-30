
 import sys
 fin = sys.stdin
 T = int(fin.readline())
 for case in range(1,T+1):
     board = []
     N, M = map(int, fin.readline().split())
     for i in range(N):
         board.append(list(map(int, fin.readline().split())))
     
     row_min = [100]*N
     row_max = [0]*N
     col_min = [100]*M
     col_max = [0]*M
 
     for i in range(N):
         for j in range(M):
             v = board[i][j]
             row_min[i] = min(v, row_min[i])
             row_max[i] = max(v, row_max[i])
             col_min[j] = min(v, col_min[j])
             col_max[j] = max(v, col_max[j])
 
 
     possible = True
     for i in range(N):
         for j in range(M):
             v = board[i][j]
             if v != row_max[i] and v != col_max[j]:
                 possible = False
                 break
 
 
     print("Case #%d: %s" % (case, possible and "YES" or "NO"))
 
 
 
