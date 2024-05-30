__author__ = 'jrokicki'
 
 import sys
 RL = lambda: sys.stdin.readline().strip()
 IA = lambda: map(int, RL().split(" "))
 LA = lambda: map(long, RL().split(" "))
 FA = lambda: map(float, RL().split(" "))
 
 T = int(sys.stdin.readline())
 
 def clear(R,C,b, x, y):
     b = b[:]
     n = 0
     for i in range(max(0,x-1), min(R,x+2)):
         for j in range(max(0,y-1), min(C, y+2)):
             if b[C*i+j] == '*':
                 n += 1
                 b = b[:C*i+j] + '.' + b[C*i+j+1:]
     return b, n
 mem = dict()
 def pb(R,C,b):
     for x in range(R):
         print b[x*C:x*C+C]
 
 def board(R,C,b,x,y,M,m):
     global mem
     print x
     key = (R,C,b,M,x,y,m)
     if key in mem: return mem[key]
     if x >= R or y >= C:
         mem[key] = None
     else:
         lb = b
         n = 0
         good = False
         for i in range(y,C):
             nb,nn = clear(R,C, lb, x, i)
             n += nn
             if m - n - M == 0:
                 mem[key] = nb
                 good = True
                 break
             elif m - n - M < 0:
                 break
             lb = bb
         mem[key] = board(R,C,bb,M,x+1,0,m-n)
     return mem[key]
 
 for CASE in range(T):
     R,C,M = IA()
     IMPOSSIBLE = "Impossible"
 
     b = ""
     cleared = R*C-M
     for x in range(R):
         b += "*" * C
     if M == R*C-1:
         b = "c" + b[1:]
         answer = b
     else:
         good = False
         x,y = 0,0
         q = [(b,0,0,0)]
         mem = {}
         while not good and q:
             board,total_cleared,x,y = q.pop(0)
             if (board,total_cleared,x,y) in mem:
                 continue
             mem[(board,total_cleared,x,y)] = True
             if x >= R: continue
             if y >= C:
                 q.append((last_board,total_cleared,x+1,0))
                 continue
             last_board = board
             new_board, cleared_mines = clear(R,C,last_board,x,y)
             total_cleared += cleared_mines
 
             if total_cleared == cleared:
                 good = True
                 last_board = new_board
                 q = []
                 break
             elif total_cleared - cleared == -1:
                 q.append((new_board,total_cleared,x,y+1))
                 q.append((new_board,total_cleared,x+1,0))
                 q.append((last_board,total_cleared-cleared_mines,x+1,0))
             elif total_cleared > cleared:
                 q.append((last_board,total_cleared-cleared_mines,x+1,0))
             else:
                 q.append((new_board,total_cleared,x,y+1))
             last_board = new_board
         if good:
             answer = last_board
         else:
             answer = None
     if not answer:
         answer = "Impossible"
     else:
         b = ""
         for x in range(R):
             b += answer[x*C:x*C+C] + "\n"
         answer = "c" + b[1:-1]
     print "Case #%d:\n%s" % (CASE+1, answer)
 
