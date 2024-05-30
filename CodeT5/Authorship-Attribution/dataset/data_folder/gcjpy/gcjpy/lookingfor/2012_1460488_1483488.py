T = int(raw_input())
 
 def isRecycle(x, y, d):
     k = 10**(d-1)
     for i in xrange(ndigits):
         y = k*(y%10) + y/10
         if x == y:
             return True
     return False
 
 for z in xrange(1, T+1):
     res = 0
     A, B = map(int, raw_input().split())
     ndigits = len(str(A))
     for i in xrange(A, B):
         for j in xrange(i+1, B+1):
            if isRecycle(i, j, ndigits):
                res += 1
     print "Case #%d:" % z, res