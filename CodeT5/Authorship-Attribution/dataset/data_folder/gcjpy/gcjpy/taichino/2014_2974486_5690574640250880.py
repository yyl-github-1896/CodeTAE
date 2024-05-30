# -*- coding: utf-8 -*-
 
 import sys
 
 
 def show_board(board):
     for row in board:
         print ''.join(row)
 
 
 N = int(sys.stdin.readline())
 
 for T in range(1, N+1):
     (R, C, M) = map(int, sys.stdin.readline().split(' '))
     E = R*C-M # empty
     possible, reverse, need_adjust, column_base = (False, False, False, False)
     if C > R:
         (R, C) = (C, R)
         reverse = True
 
     #
     # judgement
     #
     W = 0
     lastRow = 0
     if E == 0:
         pass
     elif E == 1 or M == 0:
         W = C
         possible = True
     elif C == 1:
         W = 1
         if E > 0:
             possible = True
     elif C == 2:
         W = 2
         lastRow = int(E / 2) + 1   # 1 base
         if E % 2 == 0 and E >= 4:
             possible = True
     elif C >= 3:
         for w in range(2, C+1):
             lastRow = int(E / w) + 1   # 1 base
             if lastRow > R: continue
             lastRowNum = E % w
             
             if lastRow == 2 and lastRowNum == 0:
                 pass
             elif lastRow == 2:   # lastRow == 1 => impossible
                 if lastRowNum == 0:
                     W = w
                     possible = True
                     break
             elif lastRow >= 3:
                 if lastRowNum >= 2 or lastRowNum == 0:
                     W = w
                     possible = True
                     break
                 elif C >= 4 and lastRowNum == 1 and R >= 3:
                     W = w
                     possible = True
                     need_adjust = True
                     break
         if not possible:
             for w in range(2, R+1):
                 lastRow = int(E / w) + 1   # 1 base
                 if lastRow > R: continue
                 lastRowNum = E % w
                 if lastRow == 2 and lastRowNum == 0:
                     pass
                 elif lastRow == 2:   # lastRow == 1 => impossible
                     if lastRowNum == 0:
                         W = w
                         possible = True
                         column_base = True
                         break
                 elif lastRow >= 3:
                     if lastRowNum >= 2 or lastRowNum == 0:
                         W = w
                         possible = True
                         column_base = True
                         break
                     elif C >= 4 and lastRowNum == 1 and R >= 3:
                         W = w
                         possible = True
                         need_adjust = True
                         column_base = True
                         break
                                 
     if not possible:
         if reverse:
             R, C = (C, R)        
         ans = 'Impossible %sx%s M=%s' % (R, C, M)
         # ans = 'Impossible'
         print 'Case #%(T)s: %(ans)s' % locals()
         continue
 
     #
     # make board
     #
     board = [['*'] * C for i in range(R)]
     for i in range(E):
         if not column_base:
             c = i % W
             r = i / W
         else:
             r = i % W
             c = i / W            
         board[r][c] = '.'
     if need_adjust:
         board[lastRow-1][1], board[lastRow-2][-1] = board[lastRow-2][-1], board[lastRow-1][1]
     if reverse:
         board = map(list, zip(*board))
         R, C = (C, R)
 
     clicked = False
     for r in range(R):
         if clicked: break
         for c in range(C):
             cell = board[r][c]
             if cell != '.': continue
             if E == 1:
                 board[r][c] = 'c'
                 clicked = True
                 break
             
             if r >= 1  and c >= 1  and board[r-1][c-1] == '*': continue
             if r >= 1              and board[r-1][c]   == '*': continue
             if r >= 1  and c < C-1 and board[r-1][c+1] == '*': continue
             if             c >= 1  and board[r][c-1]   == '*': continue
             if             c < C-1 and board[r][c+1]   == '*': continue
             if r < R-1 and c >= 1  and board[r+1][c-1] == '*': continue
             if r < R-1             and board[r+1][c]   == '*': continue
             if r < R-1 and c < C-1 and board[r+1][c+1] == '*': continue
             board[r][c] = 'c'
             clicked = True
             break
 
     #
     # show answer
     #
     ans = 'Possible' if possible else 'Impossible'
     print 'Case #%(T)s:' % locals()
     show_board(board)
