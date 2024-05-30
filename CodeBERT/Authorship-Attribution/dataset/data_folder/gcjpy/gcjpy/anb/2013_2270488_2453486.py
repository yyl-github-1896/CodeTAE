from sys import stdin
 
 def won(x, o, t):
     if x == 4 or (x == 3 and t == 1):
         return 1
     elif o == 4 or (o == 3 and t == 1):
         return 2
 
 def check(board, BOARD_SIZE, RESULTS):
     d = 0
     for i in xrange(BOARD_SIZE):
         x = board[i].count('X')
         o = board[i].count('O')
         t = board[i].count('T')
         d += board[i].count('.')
         w = won(x, o, t)
         if w:
             return w
     for i in xrange(BOARD_SIZE):
         vertical = [ board[j][i] for j in xrange(BOARD_SIZE) ]
         x = vertical.count('X')
         o = vertical.count('O')
         t = vertical.count('T')
         w = won(x, o, t)
         if w:
             return w
     x, o, t = 0, 0, 0
     for i in xrange(BOARD_SIZE):
         if board[i][i] == 'X':
             x += 1
         elif board[i][i] == 'O':
             o += 1
         elif board[i][i] == 'T':
             t += 1
     w = won(x, o, t)
     if w:
         return w    
     x, o, t = 0, 0, 0
     for i in xrange(BOARD_SIZE):
         if board[i][BOARD_SIZE - i - 1] == 'X':
             x += 1
         elif board[i][BOARD_SIZE - i - 1] == 'O':
             o += 1
         elif board[i][BOARD_SIZE - i - 1] == 'T':
             t += 1
     w = won(x, o, t)
     if w:
         return w
     if d == 0:
         return 3
     else:
         return 4
     
 def main():
     BOARD_SIZE = 4
     RESULTS = 'X won', 'O won', 'Draw', 'Game has not completed'
 
     T = int(stdin.readline())
     for Ti in xrange(T):
         board = []
         for i in xrange(BOARD_SIZE):
             board.append(list(stdin.readline().rstrip()))
         print 'Case #{}: {}'.format(Ti + 1, RESULTS[check(board, BOARD_SIZE, RESULTS) - 1])    
         stdin.readline()
         
 main()
