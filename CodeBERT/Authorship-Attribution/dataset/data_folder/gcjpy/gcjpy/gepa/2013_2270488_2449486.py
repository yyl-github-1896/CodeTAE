import sys
 
 
 def compute(N, M, a):
     rows = [0] * N
     cols = [0] * M
     for r in xrange(N):
         rows[r] = 0
         for c in xrange(M):
             if a[r][c] > rows[r]:
                 rows[r] = a[r][c]
     for c in xrange(M):
         cols[c] = 0
         for r in xrange(N):
             if a[r][c] > cols[c]:
                 cols[c] = a[r][c]
     for r in xrange(N):
         for c in xrange(M):
             if a[r][c] < rows[r] and a[r][c] < cols[c]:
                 return "NO"
     return "YES"
 
 
 def parse():
     N, M = map(int, sys.stdin.readline().strip().split())
     a = []
     for i in xrange(N):
         a.append(map(int, sys.stdin.readline().strip().split()))
     return N, M, a,
 
 
 if __name__ == "__main__":
     sys.setrecursionlimit(100000)
     T = int(sys.stdin.readline().strip())
     count = 1
     part = 0
     if len(sys.argv) == 3:
         part = int(sys.argv[1])
         count = int(sys.argv[2])
     for i in xrange(T):
         data = parse()
         if i * count >= part * T and i * count < (part + 1) * T:
             result = compute(*data)
             print "Case #%d: %s" % (i + 1, result)
