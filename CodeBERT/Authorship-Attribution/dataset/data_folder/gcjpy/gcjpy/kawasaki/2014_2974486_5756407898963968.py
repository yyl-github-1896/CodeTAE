# -*- coding: utf-8 -*-
 
 T = int(raw_input())
 for test_case in xrange(1, T + 1):
     N1 = int(raw_input())
     for i in xrange(4):
         if i + 1 == N1:
             R1 = map(int, raw_input().split(' '))
         else:
             raw_input()
     N2 = int(raw_input())
     for i in xrange(4):
         if i + 1 == N2:
             R2 = map(int, raw_input().split(' '))
         else:
             raw_input()
     assert 1 <= N1 <= 4
     assert 1 <= N2 <= 4
     assert len(R1) == len(R2) == 4
 
     num = set(R1) & set(R2)
     if len(num) == 1:
         answer = num.pop()
     elif 1 < len(num):
         answer = 'Bad magician!'
     else:
         answer = 'Volunteer cheated!'
     print 'Case #{}: {}'.format(test_case, answer)
