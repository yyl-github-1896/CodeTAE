# -*- coding: utf-8 -*-
 
 T = int(raw_input())
 for test_case in xrange(1, T + 1):
     R, C, M = map(int, raw_input().split())
     N = R * C
     B = N - M
 
     W, H = (C, R) if R <= C else (R, C)
 
     if H == 1:
         answer = [['c'] + ['.'] * (B - 1) + ['*'] * M]
     elif M == N - 1:
         answer = [['*'] * W for r in xrange(H)]
         answer[0][0] = 'c'
     elif B < 4 or B in (5, 7):
         answer = None
     elif H == 2:
         if M % 2 == 0:
             bw = B / 2
             answer = [
                 ['c'] + ['.'] * (bw - 1) + ['*'] * (W - bw),
                 ['.'] * bw + ['*'] * (W - bw),
             ]
         else:
             answer = None
     else:
         answer = [['*'] * W for y in xrange(H)]
         answer[0][0] = 'c'
         answer[0][1] = answer[1][0] = answer[1][1] = '.'
         left = B - 4
         if 2 <= left:
             answer[0][2] = answer[1][2] = '.'
             left -= 2
         if 2 <= left:
             answer[2][0] = answer[2][1] = '.'
             left -= 2
 
         x = y = 3
         while (x < W or y < H) and 2 <= left:
             if x < W and 2 <= left:
                 answer[0][x] = answer[1][x] = '.'
                 left -= 2
                 x += 1
             if y < H and 2 <= left:
                 answer[y][0] = answer[y][1] = '.'
                 left -= 2
                 y += 1
 
         y = 2
         while 0 < left and y < H:
             x = 2
             while 0 < left and x < W:
                 answer[y][x] = '.'
                 left -= 1
                 x += 1
             y += 1
 
     if answer is None:
         answer = 'Impossible'
     else:
         if W == R:
             answer = map(list, zip(*answer))
         assert len(answer) == R
         assert len(answer[0]) == C
         assert sum(row.count('*') for row in answer) == M
 #        # DEBUG
 #        h = len(answer)
 #        w = len(answer[0])
 #        for y in xrange(h):
 #            for x in xrange(w):
 #                if answer[y][x] in '.c':
 #                    count = 0
 #                    for dy in (-1, 0, 1):
 #                        for dx in (-1, 0, 1):
 #                            if (
 #                                0 <= x + dx < w and
 #                                0 <= y + dy < h and
 #                                answer[y + dy][x + dx] == '*'
 #                            ):
 #                                count += 1
 #                    answer[y][x] = str(count)
         answer = '\n'.join([''.join(row) for row in answer])
     print 'Case #{}:\n{}'.format(test_case, answer)
