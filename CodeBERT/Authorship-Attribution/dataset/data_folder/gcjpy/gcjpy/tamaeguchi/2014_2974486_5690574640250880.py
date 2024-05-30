#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem C. Minesweeper Master
 # https://code.google.com/codejam/contest/2974486/dashboard#s=p2
 #
 
 import sys
 
 
 def check(R, C, M, _board):
     # deepcopy
     board = [line[:] for line in _board]
 
     pos = [(0, 0)]
     while pos:
         row, col = pos.pop()
         # neighbor cell list
         neighbor = []
         for r in (-1, 0, 1):
             r += row
             for c in (-1, 0, 1):
                 c += col
                 if r >= 0 and r < R and c >= 0 and c < C:
                     neighbor.append((r, c))
         # count bomb
         count = len([1 for r, c in neighbor if board[r][c] == '*'])
         board[row][col] = str(count)
         # push next cell
         if count == 0:
             for r, c in neighbor:
                 if board[r][c] == '.':
                     pos.append((r, c))
 
     flat = ''.join(''.join(line) for line in board)
     result = not flat.count('.')
     if not result and False: # for DEBUG
         print '-' * 20
         print R, C, M
         print '\n'.join(''.join(line) for line in _board)
         print '-' * 20
     assert flat.count('*') == M
     return result
 
 
 def solve(R, C, M):
     # initialize
     board = [['.'] * C for row in range(R)]
     board[0][0] = 'c'
     row = R
     col = C
     mine = M
 
     # phase 1: right edge, bottom edge
     while mine:
         if 0 < row <= col and mine >= row:
             for r in range(row):
                 board[row - r - 1][col - 1] = '*'
             mine -= row
             col -= 1
         elif 0 < col <= row and mine >= col:
             for c in range(col):
                 board[row - 1][col - c - 1] = '*'
             mine -= col
             row -= 1
         else:
             break
 
     # phase 2:
     if mine:
         #print '\n'.join(''.join(line) for line in board)
         #print 'left', mine
         while mine and row > 2:
             for r in range(min(mine, row - 2)):
                 board[row - r - 1][col - 1] = '*'
                 mine -= 1
             col -= 1
         while mine and col > 2:
             for c in range(min(mine, col - 2)):
                 board[row - 1][col - c - 1] = '*'
                 mine -= 1
             row -= 1
 
     # phase 3
     if mine:
         # col == row == 2
         if mine:
             board[1][1] = '*'
             mine -= 1
         if mine:
             board[1][0] = '*'
             mine -= 1
         if mine:
             board[0][1] = '*'
             mine -= 1
 
     assert mine == 0
     return '\n'.join(''.join(line) for line in board) if check(R, C, M, board) else 'Impossible'
 
 
 def main(IN, OUT):
     T = int(IN.readline())
     for index in range(T):
         R, C, M = map(int, IN.readline().split())
         OUT.write('Case #%d:\n%s\n' % (index + 1, solve(R, C, M)))
 
 
 def makesample(maxSize=5, T=230):
     import random
     print T
     for index in range(T):
         R = random.randint(1, maxSize)
         C = random.randint(1, maxSize)
         print R, C, random.randint(0, R * C - 1)
 
 
 def makesample():
     pattern = []
     for R in range(1, 5+1):
         for C in range(1, 5+1):
             for M in range(R * C):
                 pattern.append((R, C, M))
     print len(pattern)
     for R, C, M in pattern:
         print R, C, M
 
 
 if __name__ == '__main__':
     if '-makesample' in sys.argv[1:]:
         makesample()
     else:
         main(sys.stdin, sys.stdout)
 
