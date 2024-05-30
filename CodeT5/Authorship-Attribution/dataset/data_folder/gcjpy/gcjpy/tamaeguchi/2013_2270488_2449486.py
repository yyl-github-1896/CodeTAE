#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem B. Lawnmower
 # https://code.google.com/codejam/contest/2270488/dashboard#s=p1
 #
 
 import sys
 
 
 def solve(board):
     vboard = []
     for m in range(len(board[0])):
         vboard.append([board[n][m] for n in range(len(board))])
 
     for n in range(len(board)):
         for m in range(len(board[n])):
             h = board[n][m]
             if h < max(board[n]) and h < max(vboard[m]):
                 return 'NO'
     return 'YES'
 
 
 def main(IN, OUT):
     T = int(IN.readline())
     for index in range(T):
         N, M = map(int, IN.readline().split())
         field = [map(int, IN.readline().split()) for n in range(N)]
         OUT.write('Case #%d: %s\n' % (index + 1, solve(field)))
 
 
 def makesample(NMmax=100, amax=100, T=100):
     import random
     print T
     for index in range(T):
         N = random.randint(1, NMmax)
         M = random.randint(1, NMmax)
         print N, M
         for n in range(N):
             print ' '.join(str(random.randint(1, amax)) for m in range(M))
 
 
 if __name__ == '__main__':
     if '-makesample' in sys.argv[1:]:
         makesample()
     else:
         main(sys.stdin, sys.stdout)
 
