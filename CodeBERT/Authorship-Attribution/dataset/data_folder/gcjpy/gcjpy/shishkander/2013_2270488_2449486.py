from itertools import izip
 
 def CASE(IN):
     def rstr(): return IN.readline().strip()
     def rint(): return int(rstr())
     def rints(): return map(int, rstr().split())
     def nrints(N): return [rints() for i in xrange(N)]
     N, M = rints()
     A = nrints(N)
     R = [max(row) for row in A]
     C = [max(col) for col in izip(*A)]
     for i, r in enumerate(R):
         for j, c in enumerate(C):
             if A[i][j] != min(r,c):
                 return "NO"
     return "YES"
 
 def RUN(IN, OUT):
     t = int(IN.readline().strip())
     for i in xrange(1,t+1):
         OUT.write("Case #%i: %s\n" % (i, CASE(IN)))
 
 if __name__ == "__main__":
     import sys
     RUN(sys.stdin, sys.stdout)
