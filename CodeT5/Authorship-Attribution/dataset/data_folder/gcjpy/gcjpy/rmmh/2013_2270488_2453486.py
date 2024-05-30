import sys
 #sys.stdin = open("a_example.in")
 
 n_cases = input()
 
 def xwin(s):
     return all(c in 'XT' for c in s)
 
 def owin(s):
     return all(c in 'OT' for c in s)
 
 for case in xrange(1, n_cases + 1):
     board = [raw_input().strip() for _ in xrange(4)]
     raw_input()
 
     board_t = zip(*board)
 
     #print board, board_t
 
     x_win = False
     o_win = False
     full = not any('.' in line for line in board)
 
     diag_nw = [board[x][x] for x in range(4)]
     diag_ne = [board[x][3-x] for x in range(4)]
 
     #print diag_nw, diag_ne
 
     if xwin(diag_nw) or xwin(diag_ne):
         x_win = True
     if owin(diag_nw) or owin(diag_ne):
         o_win = True
 
     for line, line_t in zip(board, board_t):
         if xwin(line) or xwin(line_t):
             x_win = True
         if owin(line) or owin(line_t):
             o_win = True
 
     out = 'Game has not completed'
     if x_win:
         out = 'X won'
     elif o_win:
         out = 'O won'
     elif full:
         out = 'Draw'
 
     print "Case #%d: %s" % (case, out)
