import math
 
 fin = open('C-small-attempt0.in', 'r')
 fout = open('ass3.out', 'w')
 
 T = int(fin.readline())
 
 def perfsq(n):
     sq = int(math.sqrt(n))
     if n == sq * sq:
         return sq
     return 0
 
 def palindrome(n):
     s = str(n)
     return (s == s[::-1])
 
 def getpal(n):
     if n == 1:
         for i in range(10):
             yield i
     else:
         n2 = n / 2
         for x in xrange(10 ** (n2 - 1), 10 ** n2):
             s = str(x)
             if n % 2:
                 for i in range(10):
                     ns = s + str(i) + s[::-1]
                     yield int(ns)
             else:
                 ns = s + s[::-1]
                 yield int(ns)
 
 for i in range(T):
     A, B = map(int, fin.readline().split())
 
     ret = 0
     for j in range(len(str(A)), len(str(B)) + 1):
         for x in getpal(j):
             if x < A:
                 continue
             if x > B:
                 break
             sq = perfsq(x)
             if sq and palindrome(sq):
                 ret += 1
     fout.write('Case #%i: %i\n' % (i + 1, ret))
