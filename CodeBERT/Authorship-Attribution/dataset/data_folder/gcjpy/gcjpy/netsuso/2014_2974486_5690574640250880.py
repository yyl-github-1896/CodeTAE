#!/usr/bin/python3
 #
 # Algorithm:
 # - For boards with one row: you need at least 1 free cells
 # - For boards with two rows, you need either 1 or at least 4 free cells
 #   - It needs to be an even number!
 # - For general boards, you need either 1 or at least 4 free cells (except 5 or 7)
 #
 # - To fill the board, you cannot have a row or a column with only one
 #   free cell, so you fill it in groups of two.
 #
 #   - First you start with the minimum of 4:
 #       c . * * * *
 #       . . * * * *
 #       * * * * * *
 #
 #   - Then you fill next columns and rows two by two:
 #       c . % * * *
 #       . . % * * *
 #       * * * * * *
 #
 #       c . . * * *
 #       . . . * * *
 #       % % * * * *
 #
 #       c . . % * *
 #       . . . % * *
 #       . . * * * *
 #
 #   - In case there's a pending free cell, you simply fill it in the inner board:
 #       c . . . * *
 #       . . . . * *
 #       . . % * * *
 #
 #   - In case you fill the outer border, you simply start filling the inner board:
 #       c . . . . %
 #       . . . . . %
 #       . . * * * *
 #
 #       c . . . . .
 #       . . . . . .
 #       . . % * * *
 #
 
 import sys
 
 ncases = int(sys.stdin.readline().strip())
 
 def print_board(r, c, free):
     board = {}
     for row in range(0, r):
         board[row] = {}
         for col in range(0, c):
             board[row][col] = '*'
 
     pending = free
 
     if free == 1:
         board[0][0] = '.'
     elif r == 1 or c == 1:
         for row in range(0, r):
             for col in range(0, c):
                 if pending > 0:
                     pending -= 1
                     board[row][col] = '.'
     else:
         for row in range(0,2):
             for col in range(0,2):
                 board[row][col] = '.'
         pending -= 4
         col=2
         row=2
 
         # First fill the outer border with groups of two
         while pending >= 2 and (col<c or row<r):
             if pending >= 2 and col<c:
                 board[0][col] = '.'
                 board[1][col] = '.'
                 col += 1
                 pending -= 2
             if pending >= 2 and row<r:
                 board[row][0] = '.'
                 board[row][1] = '.'
                 row += 1
                 pending -= 2
 
         # Now fill the inner board with the remaining free cells
         for row in range(2, r):
             for col in range(2, c):
                 if pending > 0:
                     board[row][col] = '.'
                     pending -= 1
 
     # The clicked one is always on the top left corner
     board[0][0] = 'c'
 
     # Finally print the board
     for row in range(0, r):
         line = ''
         for col in range(0, c):
             line += board[row][col]
         print(line)
 
 
 for t in range(1, ncases+1):
     values = sys.stdin.readline().strip().split()
     r = int(values[0])
     c = int(values[1])
     m = int(values[2])
 
     cells = r * c
     free = cells - m
 
     possible = False
 
     if r == 1 or c == 1:
         if free >= 1:
             possible = True
     elif r == 2 or c == 2:
         if free == 1 or (free >= 4 and free%2 == 0):
             possible = True
     else:
         if free == 1 or (free >= 4 and free != 5 and free != 7):
             possible = True
 
     print("Case #{0}:".format(t))
 
     if possible:
         print_board(r, c, free)
     else:
         print("Impossible")
