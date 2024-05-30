def line_status(line):
     s = set(line)
     if '.' in s:
         return 'I'
     if len(s) == 1 or (len(s) == 2 and 'T' in s):
         player = s.pop()
         while player == "T":
             player = s.pop()
         return player
     return 'D'
 
 def grid_status(grid):
     lines = grid
     columns = []
     for i in range(4):
         columns.append([])
         for j in range(4):
             columns[-1].append(grid[j][i])
     lines.extend(columns)
     lines.append([grid[i][i] for i in range(4)])
     lines.append([grid[i][3-i] for i in range(4)])
     incomplete = False
     for l in lines:
         s = line_status(l)
         if s == 'I':
             incomplete = True
         elif s in ('X', 'O'):
             return s + " won"
     if incomplete:
         return "Game has not completed"
     return "Draw"
 
 if __name__ == "__main__":
     T = int(raw_input())
     for i in range(1, T+1):
         grid = [raw_input() for j in range(4)]
         if i < T:
             raw_input()
         print "Case #%d: %s" % (i, grid_status(grid))
     
