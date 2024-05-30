
 def check(grid, n, m):
     for i in range(n):
         for j in range(m):
             if neighbor(grid,i,j,n,m):
                 return False
     return True
 
 def neighbor(grid,i,j,n,m):
     u = not i
     d = not (n-i-1)
     l = not j
     r = not (m-j-1)
     if n == 1:
         return False
     if m == 1:
         return False
     if i > 0:
         for k in range(i,-1,-1):
             if grid[k][j] > grid[i][j]:
                 u = 1
             
     if i < n-1:
         for k in range(i,n):
             if grid[k][j] > grid[i][j]:
                 d = 1
         
     if j > 0:
         for k in range(j,-1,-1):
             if grid[i][k] > grid[i][j]:
                 l = 1
         
     if j < m-1:
         for k in range(j,m):
             if grid[i][k] > grid[i][j]:
                 r = 1
     return (u*d*l*r)
         
 
 dat = raw_input().split()
 c = int(dat.pop(0))
 data = [int(e) for e in dat]
 index = 0
 t = 0
 while t < c:
     n = data[index]
     m = data[index+1]
     index += 2
     grid = []
     for i in range(n):
         grid.append(data[index:index+m])
         index += m
     if check(grid, n, m):
         print 'Case #%i: YES'%(t+1)
     else:
         print 'Case #%i: NO'%(t+1)
     t += 1
