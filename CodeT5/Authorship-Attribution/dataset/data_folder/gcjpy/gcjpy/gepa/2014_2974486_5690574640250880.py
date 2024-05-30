import sys
 
 
 DX = (-1, -1, -1, 0, 1, 1, 1, 0)
 DY = (-1, 0, 1, 1, 1, 0, -1, -1)
 
 
 def compute(R, C, M):
     if M == 0:
         return empty(R, C)
     free = R * C - M
     if free == 1:
         return single_free(R, C)
     if R == 1:
         return single_row(C, M)
     if C == 1:
         return single_column(R, M)
     if R == 2:
         return two_rows(C, M)
     if C == 2:
         return two_columns(R, M)
     if free in (2,3,5,7):
         return "\nImpossible"
     return at_least_three(R, C, M)
 
 
 def make_board(R, C, default='.'):
     return [[default for j in xrange(C)] for i in xrange(R)]
 
 
 def to_string(board):
     s = ""
     for i in xrange(len(board)):
         s += '\n' + ''.join(board[i])
     return s
 
         
 def empty(R, C):
     board = make_board(R, C)
     board[0][0] = 'c'
     return to_string(board)
 
 
 def single_free(R, C):
     board = make_board(R, C, default='*')
     board[0][0] = 'c'
     return to_string(board)
 
 
 def single_row(C, M):
     board = make_board(1, C)
     board[0][0] = 'c'
     for i in xrange(M):
         board[0][C - 1 - i] = '*'
     return to_string(board)
 
 
 def single_column(R, M):
     board = make_board(R, 1)
     board[0][0] = 'c'
     for i in xrange(M):
         board[R - 1 - i][0] = '*'
     return to_string(board)
 
 
 def two_rows(C, M):
     if M % 2 != 0:
         return "\nImpossible"
     if 2 * C - M < 4:
         return "\nImpossible"
     board = make_board(2, C)
     for i in xrange(M / 2):
         board[0][C - 1 - i] = '*'
         board[1][C - 1 - i] = '*'
     board[0][0] = 'c'
     return to_string(board)
 
 
 def two_columns(R, M):
     if M % 2 != 0:
         return "\nImpossible"
     if 2 * R - M < 4:
         return "\nImpossible"
     board = make_board(R, 2)
     for i in xrange(M / 2):
         board[R - 1 - i][0] = '*'
         board[R - 1 - i][1] = '*'
     board[0][0] = 'c'
     return to_string(board)
 
 
 def finalize(R, C, M, board):
     mines = 0
     for i in xrange(R):
         for j in xrange(C):
             if board[i][j] == '0':
                 continue
             empty = False
             for d in xrange(8):
                 if i + DX[d] < 0 or i + DX[d] >= R or j + DY[d] < 0 or j + DY[d] >= C:
                     continue
                 if board[i + DX[d]][j + DY[d]] == '0':
                     empty = True
                     break
             if empty:
                 board[i][j] = '.'
             else:
                 board[i][j] = '*'
                 mines += 1
     for i in xrange(R):
         for j in xrange(C):
             if board[i][j] == '0':
                 board[i][j] = '.'
     board[0][0] = 'c'
     if mines != M:
         sys.stderr.write("mines:%s expected:%s\n" % (mines, M))
     return to_string(board)
 
 
 def at_least_three(R, C, M):
     board = make_board(R, C)
     board[0][0] = '0'
     free = R * C - M
     count = 4
     if count == free:
         return finalize(R, C, M, board)
     board[0][1] = '0'
     count += 2
     if count == free:
         return finalize(R, C, M, board)
     board[1][0] = '0'
     count += 2
     if count == free:
         return finalize(R, C, M, board)
     for j in xrange(2, C - 1):
         if count + 2 > free:
             break
         board[0][j] = '0'
         count += 2
     for i in xrange(2, R - 1):
         if count + 2 > free:
             break
         board[i][0] = '0'
         count += 2
     for i in xrange(1, R - 1):
         for j in xrange(1, C - 1):
             if count == free:
                 return finalize(R, C, M, board)
             board[i][j] = '0'
             count += 1
     sys.stderr.write("empty board?\n")
     return finalize(board)
 
 
 def parse():
     R, C, M = map(int, sys.stdin.readline().strip().split())
     return R, C, M
 
 
 if __name__ == "__main__":
     sys.setrecursionlimit(100000)
     T = int(sys.stdin.readline().strip())
     for i in xrange(T):
         sys.stderr.write("case:%s\n" % (i + 1))
         data = parse()
         result = compute(*data)
         print "Case #%d: %s" % (i + 1, result)
