from copy import deepcopy
 import time
 
 def solve(W, H, M):
   board = [['*' for x in xrange(H)] for x in xrange(W)]
   board[0][0] = 'c'
   
   S = [((H*W)-1, board, 0, 0, set())]
   H -= 1
   W -= 1
   while len(S) > 0:
     state = S.pop()
     mines = state[0]
     board = deepcopy(state[1])
     x = state[2]
     y = state[3]
     visited = deepcopy(state[4])
     visited.add((x, y))
     
     if mines == M:
       s = ''
       for row in board:
         s += ''.join(row)
         s += '\n'
       return s
     
     elif mines > M:
       # Up
       if x > 0 and board[x-1][y] == '*':
         board[x-1][y] = '.'
         mines -= 1
       
       # Down
       if x < W and board[x+1][y] == '*':
         board[x+1][y] = '.'
         mines -= 1
       
       # Left
       if y > 0 and board[x][y-1] == '*':
         board[x][y-1] = '.'
         mines -= 1
       
       # Right
       if y < H and board[x][y+1] == '*':
         board[x][y+1] = '.'
         mines -= 1
       
       # Up and Left
       if x > 0 and y > 0 and board[x-1][y-1] == '*':
         board[x-1][y-1] = '.'
         mines -= 1
       
       # Up and Right
       if x > 0 and y < H and board[x-1][y+1] == '*':
         board[x-1][y+1] = '.'
         mines -= 1
       
       # Down and Left
       if x < W and y > 0 and board[x+1][y-1] == '*':
         board[x+1][y-1] = '.'
         mines -= 1
       
       # Down and Right
       if x < W and y < H and board[x+1][y+1] == '*':
         board[x+1][y+1] = '.'
         mines -= 1
       
       # Up
       if x > 0 and not (x-1, y) in visited:
         S.append((mines, board, x-1, y, visited))
       
       # Down
       if x < W and not (x+1, y) in visited:
         S.append((mines, board, x+1, y, visited))
       
       # Left
       if y > 0 and not (x, y-1) in visited:
         S.append((mines, board, x, y-1, visited))
       
       # Right
       if y < H and not (x, y+1) in visited:
         S.append((mines, board, x, y+1, visited))
       
       # Up and Left
       if x > 0 and y > 0 and not (x-1, y-1) in visited:
         S.append((mines, board, x-1, y-1, visited))
       
       # Up and Right
       if x > 0 and y < H and not (x-1, y+1) in visited:
         S.append((mines, board, x-1, y+1, visited))
       
       # Down and Left
       if x < W and y > 0 and not (x+1, y-1) in visited:
         S.append((mines, board, x+1, y-1, visited))
       
       # Down and Right
       if x < W and y < H and not (x+1, y+1) in visited:
         S.append((mines, board, x+1, y+1, visited))
   return 'Impossible'
 
 T = int(raw_input())
 for t in range(T):
   W, H, M = map(int, raw_input().split())
   print 'Case #%i:\n%s' % (t+1, solve(W, H, M).strip())
