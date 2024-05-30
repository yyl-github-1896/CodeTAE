import time
 import itertools
 
 from codejam import *
 
 
 directions = list(itertools.product([1, 0, -1], [1, 0, -1]))
 def count_neighbors(table, r, c):
     cols = len(table[0])
     rows = len(table)
     return sum(table[r + x][c + y] == "*" for x, y in directions 
                 if r + x >= 0 and c + y >= 0 and cols > c + y and rows > r + x)
 
 def is_valid(table):
     cols = len(table[0])
     rows = len(table)
     for r in xrange(rows):
         for c in xrange(cols):
             has_zero = any(table[r + x][c + y] == 0 for x, y in directions 
                             if r + x >= 0 and c + y >= 0 and cols > c + y and rows > r + x)
             if table[r][c] != "*" and not has_zero:
                 return False
 
     return True
 
 
 def draw_table(table, hide=False):
     cols = len(table[0])
     rows = len(table)
     ascii_table = ""
     for r in xrange(rows):
         for c in xrange(cols):
             if table[r][c] != "*":
                 ch = "c" if r == 0 and c == 0 else "."
                 table[r][c] = count_neighbors(table, r, c) if not hide else ch
 
             ascii_table += str(table[r][c])
 
         ascii_table += "\n"
 
     return ascii_table[:-1]
 
 def solve(R, C, M):
     r = c = 0
     current_mines = R * C
     table = [["*"] * C for k in xrange(R)]
     while M < current_mines:
         if table[r][c] == '*':
             table[r][c] = "."
             current_mines -= 1
 
         if current_mines > M and r + 1 < R and table[r+1][c] == "*":
             table[r+1][c] = "."
             current_mines -= 1
 
         draw_table(table)
         c += 1
         if c >= C:
             c = 0
             r += 1
 
     return table
 
 for i in xrange(readint()):
     R, C, M = readintarray()
 
     print "Case #%d:" % (i + 1)
     if M < (R * C) - 1:
         table = solve(R, C, M)
         if is_valid(table):
             print draw_table(table, hide=True)
         else:
             table = solve(C, R, M)
             rotated = [["*"] * C for k in xrange(R)]
             for r in xrange(R - 1, -1, -1):
                 for c in xrange(C):
                     rotated[R - r - 1][c] = table[c][r]
 
             print draw_table(rotated, hide=True) if is_valid(rotated) else "Impossible"
 
     elif M == R * C:
         print "Impossible"
 
     else:
         table = [["*"] * C for k in xrange(R)]
         table[0][0] = '.'
         print draw_table(table, hide=True)
