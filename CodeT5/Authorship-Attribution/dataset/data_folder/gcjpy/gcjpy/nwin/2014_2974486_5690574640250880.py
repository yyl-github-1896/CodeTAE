from itertools import product
 def solve():
     h, w, m = map(int, raw_input().split())
     if h == 1:
         print 'c' + '.' * (h * w - m - 1) + '*' * m
     elif w == 1:
         for c in 'c' + '.' * (h * w - m - 1) + '*' * m:
             print c
     elif h * w - m == 1:
         print 'c' + '*' * (w - 1)
         for _ in xrange(h-1):
             print '*' * w
     else:
         m = h * w - m
         for i in xrange(h-1):
             for j in xrange(w-1):
                 t = (i + 2) * 2 + (j + 2) * 2 - 4
                 r = (i + 2) * (j + 2)
                 if t <= m <= r:
                     a = [['*'] * w for _ in xrange(h)]
                     for k in xrange(i+2):
                         a[k][0] = '.'
                         a[k][1] = '.'
                     for k in xrange(j+2):
                         a[0][k] = '.'
                         a[1][k] = '.'
                     for y, x in product(range(2, i+2), range(2, j+2)):
                         if y == 1 and x == 1:
                             continue
                         if t >= m:
                             break
                         a[y][x] = '.'
                         t += 1
                     a[0][0] = 'c'
                     for s in a:
                         print ''.join(s)
                     return
         print 'Impossible'
 for t in xrange(int(raw_input())):
     print "Case #%d:" % (t + 1)
     solve()
