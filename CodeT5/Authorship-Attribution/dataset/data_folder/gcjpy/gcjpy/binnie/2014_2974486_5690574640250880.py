import sys
 
 f = open(sys.argv[1])
 T = int(f.readline())
 for test in range(T):
     R, C, M = map(int, f.readline().strip().split())
     Rorig = R
     Corig = C
     impossible = False
     grid = [['.' for i in range(C)] for j in range(R)]
     #print grid
 
     curr_coord = [0,0]
     while M > 0 and not impossible:
         #print curr_coord, M, grid
         if (C > R): # more columns - fill one in
             num_mines_in_column = R
             if M < R:
                 num_mines_in_column = min(R - 2, M)
             if num_mines_in_column <= 0:
                 impossible = True
                 break
             for ii in range(num_mines_in_column):
                 grid[curr_coord[0] + ii][curr_coord[1]] = '*'
             C -= 1
             curr_coord[1] += 1
             M -= num_mines_in_column
         else:
             num_mines_in_row = C
             if M < C:
                 num_mines_in_row = min(C - 2, M)
             if num_mines_in_row <= 0:
                 impossible = True
                 break
             for ii in range(num_mines_in_row):
                 grid[curr_coord[0]][curr_coord[1] + ii] = '*'
             R -= 1
             curr_coord[0] += 1
             M -= num_mines_in_row
 
     #print grid
     print "Case #%d:" % (test + 1)
     if impossible:
         print "Impossible"
     else:
         for ii in range(Rorig):
             for jj in range(Corig):
                 if grid[ii][jj] == '.':
                     if ii - 1 >= 0 and grid[ii-1][jj] == '*':
                         grid[ii][jj] = 'dirty'
                     elif jj - 1 >= 0 and grid[ii][jj-1] == '*':
                         grid[ii][jj] = 'dirty'
                     elif jj - 1 >= 0 and ii - 1 >= 0 and grid[ii-1][jj-1] == '*':
                         grid[ii][jj] = 'dirty'
         #print grid
 
         for ii in range(Rorig):
             for jj in range(Corig):
                 if grid[ii][jj] == 'dirty':
                     if ii + 1 < Rorig and grid[ii+1][jj] == '.':
                         grid[ii][jj] = '.'
                     elif jj + 1 < Corig and grid[ii][jj+1] == '.':
                         grid[ii][jj] = '.'
                     elif jj + 1 < Corig and ii + 1 < Rorig and grid[ii+1][jj+1] == '.':
                         grid[ii][jj] = '.'
                     else:
                         if ii != Rorig - 1 or jj != Corig - 1:
                             impossible = True
         #print grid
 
         if impossible:
             print "Impossible"
         else:
             grid[Rorig-1][Corig-1] = 'c'
 
             for ii in range(Rorig):
                 print " ".join([val for val in grid[ii]])
 
 
