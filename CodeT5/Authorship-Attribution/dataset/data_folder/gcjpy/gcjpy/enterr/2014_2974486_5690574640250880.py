#
 # Google Code Jam 2014
 # Roaund 0: C. Minesweeper Master
 # submission by EnTerr
 #
 
 '''
 Input
 The first line of the input gives the number of test cases, T. T lines follow. 
 Each line contains three space-separated integers: R, C, and M (Rows, Columns, Mines).
 
 Output
 For each test case, output a line containing "Case #x:", where x is the test case number. 
 On the following R lines, output the board configuration with C characters per line, 
 using '.' to represent an empty cell, '*' to represent a cell that contains a mine, 
 and 'c' to represent the clicked cell. If there is no possible configuration, 
 then instead of the grid, output a line with "Impossible" instead. 
 If there are multiple possible configurations, output any one of them.
 
 Limits
 0 <= M < R * C.
 
 Small dataset
 1 <= T <= 230.
 1 <= R, C <= 5.
 
 Large dataset
 1 <= T <= 140.
 1 <= R, C <= 50.
 
 Sample
 ---Input 
 5
 5 5 23
 3 1 1
 2 2 1
 4 7 3
 10 10 82
 
 ---Output 
 Case #1:
 Impossible
 Case #2:
 c
 .
 *
 Case #3:
 Impossible
 Case #4:
 ......*
 .c....*
 .......
 ..*....
 Case #5:
 **********
 **********
 **********
 ****....**
 ***.....**
 ***.c...**
 ***....***
 **********
 **********
 **********
 
 
 '''
 
 import sys
 from time import clock
 
 f = open(sys.argv[1])
 def input(): return f.readline().strip();
 
 from itertools import product, combinations
 def genBoards(R, C, M):
     #extra empty/boundary row added at the end (also reached as the one before [0])
     #each row has extra empty/boundary element at the end
     for mines in combinations( product(range(R), range(C)), M):
         board = [ ['.'] * C + [''] for _ in range(R) ]
         for row, col in mines:
             board[row][col] = '*'
         yield board + [[''] * (C+1)]
     pass
 
 def oneClickSolution(R, C, M):
     for bd in genBoards(R, C, M):
         #count number of mines
         minTile = 10
         for r in range(R):
             for c in range(C):
                 if bd[r][c] == '.':
                     n = sum(bd[r+i][c+j]=='*' for i in (-1,0,1) for j in (-1,0,1))
                     bd[r][c] = `n`
                     if n <= minTile:
                         minTile = n
                         minR, minC = r, c
         if minTile < 10:
             #use flood from a 0 square, does it reach all 0-s?
             queue = [ (minR, minC) ]
             nOpen = 0
             while queue:
                 r,c = queue.pop()
                 if bd[r][c] == '0':
                     for i in -1,0,1:
                         for j in -1,0,1:
                             if i or j: # we don't add the one we popped back
                                 queue.append( (r+i, c+j) )
                 if bd[r][c] not in '.*':
                     bd[r][c] = '.'
                     nOpen += 1
             if M + nOpen == R*C:
                 bd[minR][minC] = 'c'
                 return '\n'.join( ''.join(row[:-1]) for row in bd[:-1] )
 
     return 'Impossible'
 
 
 clk = clock()
 
 for caseNo in xrange(1, int(input())+1):
     R, C, M = map(int, input().split())
     print >>sys.stderr, caseNo, R, C, M #, oneClickSolution(R, C, M)<>'Impossible'
     print 'Case #%d:' % caseNo  
     print oneClickSolution(R, C, M)
     
 print >>sys.stderr, 'time= %.1f seconds' % (clock()-clk )
 
