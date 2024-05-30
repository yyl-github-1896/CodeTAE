T = int(input())
 
 def solve(R,C,M):
     # print('solving',R,C,M)
     if R>C:
         flipboard = solve(C,R,M)
         if flipboard:
             return [[flipboard[j][i] for j in range(C)] for i in range(R)]
         else:
             return
     if M==0:
         board = [['.']*C for i in range(R)]
         board[-1][-1] = 'c'
         return board
     if R == 1:
         board = ['*' if i<M else '.' for i in range(R*C)]
         board[-1] = 'c'
         return [board]
     if R == 2:
         if R*C==M+1:
             board = [['*']*C for i in range(R)]
             board[-1][-1] = 'c'
             return board
         if (M%2) or (M+2)==(R*C):
             return
         board = [['*' if i<(M/2) else '.' for i in range(C)] for j in range(R)]
         board[-1][-1] = 'c'
         return board
     if M>=R:
         subboard = solve(R,C-1,M-R)
         if subboard:
             return [['*']+r for r in subboard]
         return
     if (R,C,M) == (3,3,2):
         return
     k = min(M,C-2)
     board = [['*']*k+['.']*(C-k)]
     for i in range(M-k):
         board.append(['*']+['.']*(C-1))
     while len(board)<R:
         board.append(['.']*(C))
     board[-1][-1] = 'c'
     return board
     
          
     
 
 for case in range(1,T+1):
     print("Case #",case,": ",sep='')
     R,C,M = (int(x) for x in input().split())
     ans = solve(R,C,M)
     if ans:
         for r in ans:
             print(''.join(r))
     else:
         print('Impossible')
 
 
 # for M in range(36):
 #     ans = solve(6,6,M)
 #     if ans:
 #         for r in ans:
 #             print(''.join(r))
 #     else:
 #         print('Impossible')
