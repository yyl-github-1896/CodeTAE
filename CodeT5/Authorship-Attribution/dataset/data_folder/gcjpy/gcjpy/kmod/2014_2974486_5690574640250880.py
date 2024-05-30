import sys
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     T = int(f.readline())
     for _T in xrange(T):
         R, C, M = map(int, f.readline().split())
 
         # print R, C, M
         print "Case #%d:" % (_T+1)
 
         left = R * C - M
 
         if R == 1:
             s = 'c'
             s += '.' * (left - 1)
             s += '*' * M
             print s
             continue
         if C == 1:
             print 'c'
             for i in xrange(left - 1):
                 print '.'
             for i in xrange(M):
                 print '*'
             continue
 
         if left == 1:
             print 'c' + '*' * (C-1)
             for i in xrange(R-1):
                 print '*' * C
             continue
 
         if (R == 2 or C == 2) and (M % 2 == 1 or left == 2):
             print "Impossible"
             continue
         if R == 2:
             assert left not in (2, 3, 5, 7)
             assert left >= 4
             print 'c' + '.' * (left/2 - 1) + '*' * (M/2)
             print '.' + '.' * (left/2 - 1) + '*' * (M/2)
             continue
         if C == 2:
             assert left >= 4
             assert left not in (2, 3, 5, 7)
             print 'c.'
             left -= 2
             R -= 1
             while left:
                 print '..'
                 left -= 2
                 R -= 1
             assert R >= 0
             while R:
                 print '**'
                 R -= 1
             continue
 
         assert R >= 3
         assert C >= 3
 
         if left == 4:
             print 'c.' + '*' * (C-2)
             print '..' + '*' * (C-2)
             for i in xrange(R-2):
                 print '*' * C
             continue
 
         if left in (2, 3, 5, 7):
             print "Impossible"
             continue
 
         assert left >= 6
 
         cols = max(3, (left + R-1) // R)
 
         if left % cols == 1:
             assert left >= 10
 
             print 'c' + '.' * (cols - 1) + '*' * (C - cols)
             left -= cols
             R -= 1
 
             while left > cols + 1:
                 print '.' * cols + '*' * (C - cols)
                 left -= cols
                 R -= 1
             assert left == cols + 1
             print '.' * (cols - 1) + '*' * (C - cols + 1)
             print '.' * (2) + '*' * (C - 2)
             R -= 2
 
             assert R >= 0
 
             while R:
                 print '*' * C
                 R -= 1
             continue
         else:
             assert left >= 6
 
             print 'c' + '.' * (cols - 1) + '*' * (C - cols)
             left -= cols
             R -= 1
 
             while left > cols:
                 print '.' * cols + '*' * (C - cols)
                 left -= cols
                 R -= 1
             assert left >= 2
             print '.' * (left) + '*' * (C - left)
             R -= 1
 
             assert R >= 0
 
             while R:
                 print '*' * C
                 R -= 1
             continue
 
         1/0
