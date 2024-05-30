# coding: utf-8
 import sys
 import os.path
 from itertools import groupby
 
 def read(f):
     return list( int(v) for v in f.readline().split() )
 
 def answer(f, X, ans):
     out = "Case #{}: {}".format(X, ans)
     f.write(out)
     f.write("\n")
     print(out)
 
 def testcases(f):
     T = int(f.readline())
     for X in range(1, T + 1):
         N, M = read(f)
         GRASS = []
         for n in range(N):
             GRASS.append( read(f) )
         result = yield X, N, M, GRASS
 
 def main(inf, outf):
     for X, N, M, GRASS in testcases(inf):
         maxN = list( max(gn) for gn in GRASS )
         maxM = list( max( gn[m] for gn in GRASS ) for m in range(M) )
 
         ans = "YES"
         for n, m in ( (n, m) for m in range(M) for n in range(N) ):
             if ( GRASS[n][m] < maxN[n] and
                  GRASS[n][m] < maxM[m] ):
                 ans = "NO"
                 break
         
         answer(outf, X, ans)
 
 if __name__=="__main__":
     infname = sys.argv[1]
     outfname = os.path.splitext(infname)[0] + ".out"
     with open(infname, "r") as inf:
         with open(outfname, "w") as outf:
             main(inf, outf)
