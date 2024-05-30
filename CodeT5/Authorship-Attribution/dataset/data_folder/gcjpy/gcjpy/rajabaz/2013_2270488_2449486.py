def solve(grid, M, N):
     row_max = {}
     column_max = {}
     for i in range(M):
         row_max[i] = max(grid[i])
     for i in range(N):
         column_max[i] = max([grid[j][i] for j in range(M)])
     for i in range(M):
         for j in range(N):
             v = grid[i][j]
             if v < row_max[i] and v < column_max[j]:
                 return "NO"
     return "YES"
 
 if __name__ == "__main__":
     T = int(raw_input())
     for i in range(1,T+1):
         M,N = [int(x) for x in raw_input().split()]
         grid = [[int(x) for x in raw_input().split()] for j in range(M)]
         print "Case #%d: %s" % (i, solve(grid, M,N))
