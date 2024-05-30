#!/usr/bin/env python3
 # -*- encoding: utf-8 -*-
 
 
 def who_won(l):
     current = None
     for i in l:
         if i == '.':
             return None
         if not current and i in 'OX':
             current = i
         if current and current != i and i != 'T':
             return None
     return current
 
 
 def f(m):
     still = False
     for i in m:
         for j in i:
             if j == '.':
                 still = True
 
     rows = m # [[m[i][j] for i in range(4)] for j in range(4)]
     cols = [[m[i][j] for i in range(4)] for j in range(4)]
     diag = [[m[i][i] for i in range(4)], [m[3-i][i] for i in range(4)]]
 
     winner = None
 
     for l in rows + cols + diag:
         c = who_won(l)
         if c:
             winner = c + ' won'
 
     if not winner:
         if still:
             winner = 'Game has not completed'
         else:
             winner = 'Draw'
     return winner
 
 if __name__ == '__main__':
     T = int(input())
     for i in range(T):
         m = [list(input()) for k in range(4)]
         if i != T- 1:
             input()
         r = f(m)
         print('Case #{}: {}'.format(i+1, r))
