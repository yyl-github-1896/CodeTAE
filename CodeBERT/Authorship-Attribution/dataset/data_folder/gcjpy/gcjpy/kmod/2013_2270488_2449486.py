import sys
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())
     for _t in xrange(t):
         n, m = map(int, f.readline().split())
         b = []
         for i in xrange(n):
             b.append(map(int, f.readline().split()))
             assert len(b[-1]) == m
         # print b
 
         max_h = [0] * n
         max_v = [0] * m
 
         for i in xrange(n):
             for j in xrange(m):
                 t = b[i][j]
                 max_h[i] = max(max_h[i], t)
                 max_v[j] = max(max_v[j], t)
         can = True
         for i in xrange(n):
             if not can:
                 break
             for j in xrange(m):
                 t = b[i][j]
                 if max_h[i] > t and max_v[j] > t:
                     can = False
                     break
 
         print "Case #%d: %s" % (_t+1, "YES" if can else "NO")
