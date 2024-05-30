#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem A. Tic-Tac-Toe-Tomek
 # https://code.google.com/codejam/contest/2270488/dashboard#s=p0
 #
 
 import sys
 import string
 
 
 def solve(board):
     rows = [board[n:][:4] for n in range(0, len(board), 4)]
     cols = [''.join(board[step+n*4] for n in range(4)) for step in range(4)]
     corners = [''.join(board[n] for n in range(0, len(board), 5)),
                ''.join(board[n] for n in range(3, len(board)-1, 3))]
     lines = rows + cols + corners
 
     for line in lines:
         if line.replace('T', 'X') == 'XXXX':
             return 'X won'
         if line.replace('T', 'O') == 'OOOO':
             return 'O won'
     return 'Game has not completed' if '.' in board else 'Draw'
 
 
 def main(IN, OUT):
     T = int(IN.readline())
     for index in range(T):
         board = ''.join([IN.readline().strip() for row in range(4)])
         OUT.write('Case #%d: %s\n' % (index + 1, solve(board)))
         # empty line
         IN.readline()
 
 
 def makesample(T=1000):
     import random
     print T
     for index in range(T):
         board = []
         for row in range(4):
             board.append(''.join(random.choice('XO.') for col in range(4)))
         tcol = random.randint(0, 3)
         trow = random.randint(0, 3)
         board[trow] = board[trow][:tcol] + 'T' + board[trow][tcol+1:]
         print '\n'.join(board)
         print
 
 
 if __name__ == '__main__':
     if '-makesample' in sys.argv[1:]:
         makesample()
     else:
         main(sys.stdin, sys.stdout)
 
