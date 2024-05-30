def get_number_of_test_case():
     return int(raw_input().strip())
 
 def solve_case(t):
     N, M = [int(x) for x in raw_input().strip().split()]
     
     matrix = [[int(x) for x in raw_input().strip().split()] for y in range(N)]
 
     s_list = list()
     for i in range(N):
         for j in range(M):
             s_list.append([matrix[i][j], i, j,])
     s_list.sort(cmp = lambda x, y: x[0] - y[0])
 
     outcome = 'YES'
     for s in s_list:
         if matrix[s[1]][s[2]] == 0:
             continue
 
         row, col = s[1], s[2]
 
         can_do = True
         for i in range(N):
             can_do &= matrix[i][col] <= s[0]
         if can_do:
             for i in range(N):
                 matrix[i][col] = 0
             continue
 
         can_do = True
         for j in range(M):
             can_do &= matrix[row][j] <= s[0]
         if can_do:
             for j in range(M):
                 matrix[row][j] = 0
         else:
             outcome = 'NO'
             break
     
     print 'Case #%d: %s' % (t, outcome,)
 
 
 T = get_number_of_test_case()
 t = 1
 while t <= T:
     solve_case(t)
     t += 1
 
