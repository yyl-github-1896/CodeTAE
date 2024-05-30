#
 # Google Code Jam 2013
 # Round 0: A. Tic-Tac-Toe-Tomek
 # submission by EnTerr
 #
 
 '''
 Limits
 The game board provided will represent a valid state that was reached
 through play of the game Tic-Tac-Toe-Tomek as described above.
 
 Small dataset   1 = T = 10.
 Large dataset   1 = T = 1000.
 
 *** Sample Input 
 6
 XXXT
 ....
 OO..
 ....
 
 XOXT
 XXOO
 OXOX
 XXOO
 
 XOX.
 OX..
 ....
 ....
 
 OOXX
 OXXX
 OX.T
 O..O
 
 XXXO
 ..O.
 .O..
 T...
 
 OXXX
 XO..
 ..O.
 ...O
 
 ***Output 
 Case #1: X won
 Case #2: Draw
 Case #3: Game has not completed
 Case #4: O won
 Case #5: O won
 Case #6: O won
 
 '''
 
 #import psyco
 #psyco.full()
 
 import sys
 from time import clock
 
 inf = open(sys.argv[1])
 def input(): return inf.readline().strip()
 
 import re
 
 # compile "just in case" not to rely on `re` caching
 # check horizontal or vertical or diagonal type1 or diag. type2
 x_ptrn = re.compile('X{4}|X(.{4}X){3}|X(.{3}X){3}|X(.{5}X){3}')
 o_ptrn = re.compile('O{4}|O(.{4}O){3}|O(.{3}O){3}|O(.{5}O){3}')
 
 
 def check_game_status(board):
     if x_ptrn.search(board.replace('T','X')):
         return 'X won'
     elif o_ptrn.search(board.replace('T','O')):
         return 'O won'
     elif '.' not in board:
         return 'Draw'
     else:
         return 'Game has not completed'
 
 for caseNo in range(1, int(input())+1):
     #tm = clock()
     board = '|'.join(input() for _ in range(4))
     input() # skip empty line
     print 'Case #%d:' % caseNo, check_game_status(board)
     #print >>sys.stderr, caseNo, clock() - tm
 
