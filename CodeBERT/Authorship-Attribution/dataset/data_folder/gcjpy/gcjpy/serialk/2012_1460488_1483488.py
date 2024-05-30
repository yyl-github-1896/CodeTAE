#!/usr/bin/env python2.7
 
 T = int(raw_input())
 for i in xrange(T):
     values = map(int, raw_input().split())
     [N,s,p] = values[0:3]
     t = values[3:]
     answer = 0
     for note in t:
         if note < 2:
             if note >= p:
                 answer += 1
         elif note % 3 == 1 and (note-1) / 3 + 1 >= p:
             answer += 1
         elif note % 3 == 0:
             n = note / 3
             if n >= p:
                 answer += 1
             elif s > 0 and n + 1 >= p:
                 answer += 1
                 s -= 1
         elif note % 3 == 2:
             n = (note - 2) / 3
             if n + 1 >= p:
                 answer += 1
             elif s > 0 and n + 2 >= p:
                 answer += 1
                 s -= 1
     print 'Case #{0}: {1}'.format(i+1, answer)
