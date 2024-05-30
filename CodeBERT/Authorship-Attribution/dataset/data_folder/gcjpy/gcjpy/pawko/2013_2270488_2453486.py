# python 3
 import string
 import itertools
 import sys
 
 P1 = 'X'
 P2 = 'O'
 PA = 'T'
 EMPTY = '.'
 
 def no_empty_fields(board):
     for row in board:
         for field in row:
             if field==EMPTY:
                 return False
     return True
 
 def is_winning_series(board, r0, c0, dr, dc, player):
     r,c = r0,c0
     for i in range(4):
         if board[r][c] != player and board[r][c] != PA:
             return False
         r,c = r+dr,c+dc
     return True
 
 def win_condition(board, player):
     if is_winning_series(board, 0,0, 1,1, player):
         return True
     if is_winning_series(board, 0,3, 1,-1, player):
         return True
     for i in range(4):
         if is_winning_series(board, 0,i, 1,0, player):
             return True
         if is_winning_series(board, i,0, 0,1, player):
             return True
     return False
 
 def process_case(board):
     for player in {P1, P2}:
         if win_condition(board, player):
             return '{0} won'.format(player)
     if no_empty_fields(board):
         return 'Draw'
     return 'Game has not completed'
 
 def result_gen(lines):
     ncases = int(next(lines))
     for ci in range(1,ncases+1):
         board = [[ch for ch in next(lines)] for i in range(4)]
         next(lines)
         result = process_case(board)
         yield 'Case #{0}: {1}\n'.format(ci, result)
     
 def line_of_numbers(s):
     return [int(sub) for sub in s.split()]
 
 def input_gen(f_in):
     for line in f_in:
         if line.endswith('\n'):
             line = line[:-1]
         yield line
 
 def start(basename):
     infile = basename + '.in'
     outfile = basename + '.out'
     f_in = open(infile, 'r')
     f_out = open(outfile, 'w')
     f_out.writelines(result_gen(input_gen(f_in)))
     f_in.close()
     f_out.close()
 
 ##start('A-test')
 start('A-small-attempt0')
 ##start('A-large')
