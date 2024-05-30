# -*- coding: utf-8 -*-
 
 import sys
 
 N = int(sys.stdin.readline())
 
 for T in range(1, N+1):
     first_ans = int(sys.stdin.readline())
     first_grid = []
     for i in range(4):
         row = [int(v) for v in sys.stdin.readline().split(' ')]
         first_grid.append(row)
     first_list = set(first_grid[first_ans-1])
     
     second_ans = int(sys.stdin.readline())
     second_grid = []
     for i in range(4):
         row = [int(v) for v in sys.stdin.readline().split(' ')]
         second_grid.append(row)
     second_list = set(second_grid[second_ans-1])
 
     intersection = first_list.intersection(second_list)
 
     if len(intersection) == 1:
         ans = intersection.pop()
     elif len(intersection) == 0:
         ans = 'Volunteer cheated!'
     else:
         ans = 'Bad magician!'
 
     print 'Case #%(T)s: %(ans)s' % locals()
