#!/usr/bin/env python3
 # -*- encoding: utf-8 -*-
 
 
 def f(m):
     max_cols = []
     for e in zip(*m):
         max_cols.append(max(e))
 
     for r in m:
         max_row = max(r)
         for y, c in enumerate(r):
             if c != max_row and c != max_cols[y]:
                 return 'NO'
     return 'YES'
 
 if __name__ == '__main__':
     T = int(input())
     for i in range(T):
         n, m = map(int, input().split())
         r = f([input().split() for i in range(n)])
         print('Case #{}: {}'.format(i+1, r))
