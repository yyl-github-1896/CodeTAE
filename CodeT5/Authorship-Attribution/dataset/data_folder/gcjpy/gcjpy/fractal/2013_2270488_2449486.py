#! /usr/bin/python
 
 T=input()
 
 for i in range(1, T+1):
     N, M = raw_input().split()
     N, M = int(N), int(M)
     matrix = []
     for j in range(N):
         row = raw_input().split()
         assert len(row) == M
         row = [int(x) for x in row]
         matrix.append(row)
     rmax = [max(x) for x in matrix]
     matrix_t = [list(x) for x in zip(*matrix)]
     cmax = [max(x) for x in matrix_t]
     feasible = True
     for r, k in zip(matrix, range(N)):
         for c, l in zip(r, range(M)):
             if c == rmax[k]:
                 continue
             elif c == cmax[l]:
                 continue
             else:
                 break
         else:
             continue
         break
     else:
         print "Case #%d: %s" % (i, "YES")
         continue
     print "Case #%d: %s" % (i, "NO")
