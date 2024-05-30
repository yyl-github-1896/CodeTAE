import sys
 
 lines = [line.strip() for line in open(sys.argv[1])]
 count = int(lines[0])
 
 for i in xrange(count):
     R,C,M = map(int, lines[i+1].split())
     print "Case #%s:" % (i+1)
 
     w = max(R,C)
     h = min(R,C)
     X = R*C - M
     assert X > 0
 
     if X == 1:
         rows = ['c' + ('*' * (w-1))] + (h-1) * ['*' * w]
     elif h == 1:
         rows = ['c' + '.' * (X-1) + '*' * M]
     elif X == 4:
             rows = [
                 'c.' + '*' * (w-2),
                 '..' + '*' * (w-2),
             ] + ['*' * w] * (h-2)
     elif h == 2:
         if X%2 == 1 or X == 2:
             rows = None
         else:
             rows = [
                 'c' + '.' * (X/2-1) + '*' * (M/2),
                 '.' + '.' * (X/2-1) + '*' * (M/2)
             ]
     elif X <= 5 or X == 7:
         rows = None
 
     elif X%2 == 0 and X <= w*2:
         r = X/2
         rows = [
             'c' + '.' * (r - 1) + '*' * (w-r),
                   '.' * r       + '*' * (w-r),
         ] + ['*' * w] * (h-2)
 
     elif X <= w*3 and (X % 3) != 1:
         n = (X+1) / 3
         t = X - 2*n
         rows = [
             'c' + '.' * (n-1) + '*' * (w-n),
                   '.' * n     + '*' * (w-n),
                   '.' * t     + '*' * (w-t)
         ] + ['*' * w] * (h-3)
     else:
         n = X / w
         t = X % w
         if t == 1:
             rows = (
                     ['c' + (w-1) * '.']
                 +   ['.' * w] * (n-2)
                 +   ['.' * (w-1) + '*']
                 +   ['..' + '*' * (w-2)]
                 +   ['*' * w] * (h - n - 1)
             )
         else:
             k = 1 if t == 0 else 0
             rows = (
                     ['c' + (w-1) * '.']
                 +   ['.' * w] * (n-1)
                 +   ['.' * t + '*' * (w-t)] * (1 - k)
                 +   ['*' * w] * (h - n - 1 + k)
             )
 
     if rows:
         if R > C:
             rows = ["".join(row[i] for row in rows) for i in xrange(R)]
 
         for row in rows:
             print row
 
         assert len(rows) == R
         assert len(rows[0]) == C
         assert sum(1 for row in rows for col in row if col == '*') == M
 
     else:
         print "Impossible"
 
