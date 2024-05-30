def make_string(R, C, M):
     grid = [['.' for j in xrange(C)] for i in xrange(R)]
     grid[-1][-1] = 'c'
     t = M
     for i in xrange(R):
         for j in xrange(C):
             if M:
                 if forbidden(R, C, t, i, j):
                     continue
                 grid[i][j] = '*'
                 M -= 1
             else:
                 break
     s = ''
     if M:
         return 'Impossible'
     for r in grid:
         s += ''.join(r)+'\n'
     return s[:-1]
 
 def forbidden(R, C, M, i, j):
     a = M / C
     b = M % C
     if (R*C - M == 1):
         return False
 
     if i >= (R-2) and j >= (C-2):
         return True
 
     if i >= (R-2) and b:
         if b % 2:
             return True
         if j < b/2:
             return False
         else:
             return True
     return False
         
 
 f = open('Csmall.in', 'r')
 ##f = open('test.txt', 'r')
 g = open('outputC.txt', 'w')
 
 data = [[int(e) for e in line.strip("\n").split(' ')] for line in f]
 T = int(data.pop(0)[0])
 for i, case in enumerate(data):
     R, C, M = case[0], case[1], case[2]
     num_cells = R*C
     if (R-1) == 0 or (C-1) == 0:
         s = make_string(R, C, M)
         g.write('Case #%i:\n%s\n' %(i+1,s))
         continue
     else:
         s = make_string(R, C, M)
         g.write('Case #%i:\n%s\n' %(i+1, s))
         
 
 f.close()
 g.close()
