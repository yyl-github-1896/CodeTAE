#!/usr/bin/env python3
 # -*- coding: utf-8 -*-
 # Uses https://github.com/rkistner/contest-algorithms
 
 # Minesweeper is a computer game that became popular in the 1980s, and is still included in some versions of the Microsoft Windows operating system. This problem has a similar idea, but it does not assume you have played Minesweeper.
 
 # In this problem, you are playing a game on a grid of identical cells. The content of each cell is initially hidden. There are M mines hidden in M different cells of the grid. No other cells contain mines. You may click on any cell to reveal it. If the revealed cell contains a mine, then the game is over, and you lose. Otherwise, the revealed cell will contain a digit between 0 and 8, inclusive, which corresponds to the number of neighboring cells that contain mines. Two cells are neighbors if they share a corner or an edge. Additionally, if the revealed cell contains a 0, then all of the neighbors of the revealed cell are automatically revealed as well, recursively. When all the cells that don't contain mines have been revealed, the game ends, and you win.
 
 # For example, an initial configuration of the board may look like this ('*' denotes a mine, and 'c' is the first clicked cell):
 
 # *..*...**.
 # ....*.....
 # ..c..*....
 # ........*.
 # ..........
 # There are no mines adjacent to the clicked cell, so when it is revealed, it becomes a 0, and its 8 adjacent cells are revealed as well. This process continues, resulting in the following board:
 # *..*...**.
 # 1112*.....
 # 00012*....
 # 00001111*.
 # 00000001..
 # At this point, there are still un-revealed cells that do not contain mines (denoted by '.' characters), so the player has to click again in order to continue the game.
 # You want to win the game as quickly as possible. There is nothing quicker than winning in one click. Given the size of the board (R x C) and the number of hidden mines M, is it possible (however unlikely) to win in one click? You may choose where you click. If it is possible, then print any valid mine configuration and the coordinates of your click, following the specifications in the Output section. Otherwise, print "Impossible".
 
 # Input
 
 # The first line of the input gives the number of test cases, T. T lines follow. Each line contains three space-separated integers: R, C, and M.
 
 # Output
 
 # For each test case, output a line containing "Case #x:", where x is the test case number (starting from 1). On the following R lines, output the board configuration with C characters per line, using '.' to represent an empty cell, '*' to represent a cell that contains a mine, and 'c' to represent the clicked cell.
 
 # If there is no possible configuration, then instead of the grid, output a line with "Impossible" instead. If there are multiple possible configurations, output any one of them.
 
 # Limits
 
 # 0 ≤ M < R * C.
 # Small dataset
 
 # 1 ≤ T ≤ 230.
 # 1 ≤ R, C ≤ 5.
 # Large dataset
 
 # 1 ≤ T ≤ 140.
 # 1 ≤ R, C ≤ 50.
  
 
 
 import sys
 
 
 def debug(*args):
     print(*args, file=sys.stderr)
 
 fin = sys.stdin
 T = int(fin.readline())
 for case in range(1, T + 1):
     RR, CC, M = map(int, fin.readline().split())
     R, C = None, None
     blocks = RR*CC - M
     inverse = False
     if RR > CC:
         inverse = True
         R, C = CC, RR
     else:
         R, C = RR, CC
     result = None
     # Now R <= C
     if R == 1:
         # Always possible
         result = [('.' * blocks) + ('*' * M)]
     elif R == 2:
         # Possible if blocks == 1 or blocks % 2 == 0
         if blocks == 1:
             result = ['.' + ('*' * (C-1)), '*' * C]
         elif blocks % 2 == 0 and blocks != 2:
             cc = blocks // 2
             result = [('.' * cc) + ('*' * (C - cc)), ('.' * cc) + ('*' * (C - cc))] 
         else:
             result = None
     else:
         if blocks == 1:
             result = ['*' * C] * R
         elif blocks == 4:
             result = ['..' + (C-2)*'*']*2
             result += ['*'*C] * (R-2)
         elif blocks == 6:
             result = ['...' + (C-3)*'*']*2
             result += ['*'*C] * (R-2)
         for rows in range(3, R+1):
             for columns in range(rows, C+1):
                 size = rows * columns
                 if size - blocks >= 0:
                     if size - blocks <= columns - 2: 
                         result = []
                         for r in range(rows):
                             if r < rows - 1:
                                 result.append(('.' * columns) + ('*' * (C - columns)))
                             else:
                                 cc = columns - (size - blocks)
                                 result.append(('.' * cc) + ('*' * (C - cc)))
                         for r in range(R - rows):
                             result.append('*' * C)
                     elif size - blocks == columns - 1 and rows >= 4:
                         result = []
                         for r in range(rows):
                             if r < rows - 2:
                                 result.append(('.' * columns) + ('*' * (C - columns)))
                             elif r == rows - 2:
                                 cc = columns - 1
                                 result.append(('.' * cc) + ('*' * (C - cc)))
                             else:
                                 cc = 2
                                 result.append(('.' * cc) + ('*' * (C - cc)))
                         for r in range(R - rows):
                             result.append('*' * C)
                     
 
 
 
     print("Case #%d: " % (case))
     if result is None:
         debug('impossible', blocks, RR, CC)
         print("Impossible")
     else:
         mines = 0
         for r in range(RR):
             row = ''
             for c in range(CC):
                 rr, cc = r, c
                 if inverse:
                     rr, cc = c, r
                 if rr == 0 and cc == 0:
                     row += 'c'
                 else:
                     row += result[rr][cc]
                     if result[rr][cc] == '*':
                         mines += 1
             print(row)
         if mines != M:
             raise Exception("%d != %d %d x %d" % (mines, M, RR, CC))
             
 
 
