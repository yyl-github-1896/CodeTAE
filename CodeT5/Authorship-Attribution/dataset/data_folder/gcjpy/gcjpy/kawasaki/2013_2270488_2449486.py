# -*- coding: utf-8 -*-
 
 T = int(raw_input())
 for test_case_id in xrange(1, T + 1):
     N, M = map(int, raw_input().split())
     A = []
     for i in xrange(N):
         A.append(map(int, raw_input().split()))
 
     heights = reduce(lambda a, b: a | b, (set(row) for row in A))
     for y in xrange(N):
         for x in xrange(M):
             if (
                 any(A[y][j] > A[y][x] for j in xrange(M)) and
                 any(A[i][x] > A[y][x] for i in xrange(N))
             ):
                 # Found a region surrounded by higher regions.
                 print 'Case #{}: NO'.format(test_case_id)
                 break
         else:
             continue
         break
     else:
         print 'Case #{}: YES'.format(test_case_id)
