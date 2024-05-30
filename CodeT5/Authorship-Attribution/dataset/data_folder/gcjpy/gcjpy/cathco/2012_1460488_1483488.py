import sys
 
 def isRecycledPair(n, m):
     m = str(m)
     for i in range(len(m)):
         m = m[-1] + m[:-1]
         if n == int(m):
             return True
     return False
 
 T = int(sys.stdin.readline())
 for i in range(T):
     [A, B] = map(int, sys.stdin.readline().strip().split(' '))
     count = 0
     for n in range(A, B+1):
         for m in range(n, B+1):
             if n != m and isRecycledPair(n, m):
                 count += 1
     print 'Case #%s: %s' % (i + 1, count)
