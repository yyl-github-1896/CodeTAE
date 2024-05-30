
 
 INPUT = 'C-small-attempt0.in'
 OUTPUT = 'C-small-attempt0.out'
 
 
 def solve(R, C, M):
     grid = [[0 for c in range(C)] for r in range(R)]
 
     def get_cell(cell_r, cell_c):
         if not(0 <= cell_r < R):
             return None
         if not(0 <= cell_c < C):
             return None
         return grid[cell_r][cell_c]
 
     def for_each_neighbour(cell_r, cell_c, func):
         ret = []
         coords = (
             (cell_r - 1, cell_c - 1), (cell_r - 1, cell_c), (cell_r - 1, cell_c + 1),
             (cell_r, cell_c - 1), (cell_r, cell_c + 1),
             (cell_r + 1, cell_c - 1), (cell_r + 1, cell_c), (cell_r + 1, cell_c + 1)
         )
         for nb in coords:
             if get_cell(nb[0], nb[1]) is not None:
                 ret.append(func(nb[0], nb[1]))
         return ret
 
     def mark_dirty(cell_r, cell_c):
         if grid[cell_r][cell_c] != '*':
             grid[cell_r][cell_c] += 1
     
     def unmark_dirty(cell_r, cell_c):
         if grid[cell_r][cell_c] != '*':
             grid[cell_r][cell_c] -= 1
 
     def check_empty_neighbours(cell_r, cell_c):
         return (0 in for_each_neighbour(cell_r, cell_c, lambda r, c: get_cell(r, c)))
 
     def click():
         for i, row in enumerate(grid):
             for j, cell in enumerate(row):
                 if cell != '*':
                     if cell == 0 or ((R * C - M) == 1):
                         grid[i][j] = 'c'
                         return
 
     def place_mine():
         for i, row in enumerate(grid):
             for j, cell in enumerate(row):
                 if cell == '*':
                     continue
                 prevstate = grid[i][j]
                 grid[i][j] = '*'
                 for_each_neighbour(i, j, mark_dirty)
                 if not (True in for_each_neighbour(i, j, check_empty_neighbours)):
                     grid[i][j] = prevstate
                     for_each_neighbour(i, j, unmark_dirty)
                 else:
                     return True
         return False
 
     for m in range(M):
         if not place_mine():
             return 'Impossible\n'
 
     click()
 
     ret = ''
     for row in grid:
         ret = ret + ''.join(map(lambda c: '.' if isinstance(c, int) else c, row)) + '\n'
 
     return ret
 
 
 if __name__ == '__main__':
     inp = open(INPUT)
     out = open(OUTPUT, 'w')
     
     T = int(inp.readline())
 
     for case in range(T):
         sol = solve(*map(int, inp.readline().split()))
         out.write('Case #%i:\n%s' % (case + 1, sol))