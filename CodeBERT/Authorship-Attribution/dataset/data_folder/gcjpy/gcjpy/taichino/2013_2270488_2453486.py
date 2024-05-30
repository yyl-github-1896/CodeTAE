# -*- coding: utf-8 -*-
 
 import sys
 
 N = int(sys.stdin.readline())
 
 for T in range(1, N+1):
     lines = []
     completed = True
     for i in range(4):
         line = sys.stdin.readline().strip()
         if '.' in line:
             completed = False
         lines.append(line)
     sys.stdin.readline() # empty line
 
     ans = 'Draw' if completed else 'Game has not completed'
     # horizontal
     for row in range(4):
         X, O = 0, 0
         for col in range(4):
             spot = lines[row][col]
             if spot == 'O':
                 O += 1
             elif spot == 'X':
                 X += 1
             if spot == 'T':
                 O += 1
                 X += 1
         if X == 4:
             ans = 'X won'
         elif O == 4:
             ans = 'O won'
 
     # vertical
     for col in range(4):
         X, O = 0, 0
         for row in range(4):
             spot = lines[row][col]
             if spot == 'O':
                 O += 1
             elif spot == 'X':
                 X += 1
             if spot == 'T':
                 O += 1
                 X += 1
         if X == 4:
             ans = 'X won'
         elif O == 4:
             ans = 'O won'
 
     # diagonal
     X1, X2, O1, O2 = 0, 0, 0, 0
     for i in range(4):
         spot1 = lines[i][i]
         spot2 = lines[4-i-1][i]
 
         if spot1 == 'O':
             O1 += 1
         elif spot1 == 'X':
             X1 += 1
         elif spot1 == 'T':
             O1 += 1
             X1 += 1
 
         if spot2 == 'O':
             O2 += 1
         elif spot2 == 'X':
             X2 += 1
         elif spot2 == 'T':
             O2 += 1
             X2 += 1
 
     if X1 == 4 or X2 == 4:
         ans = 'X won'
     elif O1 == 4 or O2 == 4:
         ans = 'O won'
     
     
     print 'Case #%(T)s: %(ans)s' % locals()
