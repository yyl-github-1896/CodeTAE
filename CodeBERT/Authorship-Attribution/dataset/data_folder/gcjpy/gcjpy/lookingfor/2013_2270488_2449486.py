T = int(raw_input())
 
 def readMatrix(nlines):
     return [map(int, raw_input().split(' ')) for i in xrange(nlines)]
 
 def transpose(A):
     return map(lambda i: map(lambda line: line[i], A), xrange(len(A[0])))
 
 for z in xrange(T):
     M, N = map(int, raw_input().split(' '))
     A = readMatrix(M)
     b = map(max, A)
     c = map(max, transpose(A))
     fl = True
     for i in xrange(M):
         for j in xrange(N):
             if A[i][j] != min(b[i], c[j]):
                 fl = False
     print "Case #%d: %s" % (z+1, "YES" if fl else "NO")