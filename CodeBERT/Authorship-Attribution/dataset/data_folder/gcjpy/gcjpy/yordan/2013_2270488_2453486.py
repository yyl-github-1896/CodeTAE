#!/usr/bin/env python
 
 import itertools
 import sys
 
 
 def next_board(stream=None):
     """"""
     if stream is None:
         stream = sys.stdin
     board = []
     for line in filter(lambda line: len(line) and line[0] in '.OTX', stream):
         board.append([c for c in line.rstrip()])
         if len(board) == 4:
             break
     return board if len(board) else None
 
 
 def scan_not_completed(board):
     if any(board[i][j] == '.'
            for j in range(len(board))
            for i in range(len(board))):
         return '.'
 
 
 def check_set(s):
     s.discard('T')
     return s.pop() if len(s) == 1 and '.' not in s else None
 
 
 scan_diagonal1 = lambda board: check_set({board[i][i]
         for i in range(len(board))})
 
 scan_diagonal2 = lambda board: check_set({board[i][len(board)-1-i]
         for i in range(len(board))})
 
 scan_col = lambda board, col: check_set({board[i][col]
     for i in range(len(board))})
 
 scan_row = lambda board, row: check_set(set(board[row]))
 
 
 def determine_state(board):
     """"""
     for i in range(4):
         for s in (scan_col, scan_row):
             ret = s(board, i)
             if ret:
                 return ret
     for s in (scan_diagonal1, scan_diagonal2, scan_not_completed):
         ret = s(board)
         if ret:
             return ret
     return 'draw'
 
 
 def main():
     """"""
     with open('A-small-attempt0.in', encoding='utf-8') as f:
         for i in itertools.count(1):
             board = next_board(f)
             if board is None:
                 break
             state = determine_state(board)
             if state == 'X':
                 line = 'X won'
             elif state == 'O':
                 line = 'O won'
             elif state == 'draw':
                 line = 'Draw'
             elif state == '.':
                 line = 'Game has not completed'
             print('Case #{}: {}'.format(i, line))
 
 
 main()
