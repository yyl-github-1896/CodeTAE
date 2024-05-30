#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem *. 
 # https://code.google.com/codejam/contest/***
 #
 
 import sys
 
 
 def solve(arrange):
     board, row = arrange[0]
     before = board[row - 1]
     board, row = arrange[1]
     after = board[row - 1]
     dup = set(before) & set(after)
     if len(dup) == 1:
         return dup.pop()
     elif len(dup) >= 2:
         return 'Bad magician!'
     else:
         return 'Volunteer cheated!'
 
 
 def main(IN, OUT):
     T = int(IN.readline())
     for index in range(T):
         arrange = []
         for n in range(2):
             row = int(IN.readline())
             board = []
             for line in range(4):
                 board.append(map(int, IN.readline().split()))
             arrange.append((board, row))
         OUT.write('Case #%d: %s\n' % (index + 1, solve(arrange)))
 
 
 def makesample(T=100):
     import random
     print T
     for index in range(T):
         for n in range(2):
             print random.randint(1, 4)
             board = list(range(1, 16+1))
             random.shuffle(board)
             while board:
                 print ' '.join(map(str, board[:4]))
                 board = board[4:]
 
 
 if __name__ == '__main__':
     if '-makesample' in sys.argv[1:]:
         makesample()
     else:
         main(sys.stdin, sys.stdout)
 
