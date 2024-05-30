# -*- coding: utf-8 -*-
 
 import itertools
 
 poss = dict([(i, {}) for i in xrange(0, 30 + 1)])
 for a, b, c in itertools.product(range(10 + 1), repeat=3):
     if a <= b <= c and c - a <= 2:
         n = a + b + c
         if c - a == 2:
             poss[n]['s'] = tuple(sorted((a, b, c)))
         else:
             poss[n]['n'] = tuple(sorted((a, b, c)))
 
 
 T = int(raw_input())
 for case in xrange(1, T + 1):
     div = map(int, raw_input().split())
     N, S, p = div[:3]
     t = div[3:]
 
     ans = 0
     t.sort(reverse=True)
     for i in xrange(len(t)):
         na, nb, nc = poss[t[i]]['n']
         sa, sb, sc = poss[t[i]].get('s', (-1, -1, -1))
         if p <= nc:
             ans += 1
         elif 0 < S and p <= sc:
             ans += 1
             S -= 1
 
     print 'Case #%d: %d' % (case, ans)
 
