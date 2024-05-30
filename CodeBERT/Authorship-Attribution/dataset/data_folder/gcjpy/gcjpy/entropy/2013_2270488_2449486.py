
 def check(grid):
     if len(grid) <= 1 or len(grid[0]) <= 1:
         return True
     for r in range(len(grid)-1):
         for c in range(len(grid[r])-1):
             e1 = grid[r][c]
             e2 = grid[r][c+1]
             e3 = grid[r+1][c]
             e4 = grid[r+1][c+1]
             if (e1 > e2 and e4 > e2) or (e1 > e3 and e4 > e3):
                 return False
             if (e2 > e1 and e3 > e1) or (e2 > e4 and e3 > e4):
                 return False
     return True
 
 def removeG(grid):
     for i in range(len(grid)):
         if len(set(grid[i])) == 1 and grid[i][0] == 1 :
             del grid[i]
             return True
     return False
 
 infile = open('B-small-attempt5.in', 'Ur')
 #infile = open('test3.in', 'Ur')
 
 tests = int(infile.readline().strip())
 
 for t in range(tests):
     grid = []
     h, w = [int(x) for x in infile.readline().strip().split()]
     for i in range(h):
         row =[int(x) for x in infile.readline().strip().split()]
         grid.append(row)
 
     pass1 = check(grid)
     print("------")
     for r in grid:
         print(" ".join([str(x) for x in r]))
     while len(grid) >= 3:
         if not removeG(grid):
             break
 
     pass2 = check(grid)
     grid = [x for x in zip(*grid[::-1])]
     while len(grid) >= 3:
         if not removeG(grid):
             break
     print("------")
     for r in grid:
         print(" ".join([str(x) for x in r]))
     pass3 = check(grid)
 
 
 #   if len(grid) >= 3:
 #       grid = [row for row in grid if len(set(row)) != 1]
 #   print("------")
 #   for r in grid:
 #       print(" ".join([str(x) for x in r]))
 
     if pass1 and pass2 and pass3:
         res = 'YES'
     else:
         res = 'NO'
 
     print("Case #{0}: {1}".format(t+1,res))
 
 
