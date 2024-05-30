# coding: utf-8
 import sys
 import os.path
 import itertools
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
         A, B = read(f)
         yield X, A, B
 
 def ispalindrome(v):
     s = str(v)
     for i in range(len(s) // 2):
         if s[i] != s[-i-1]:
             return False
     return True
 
 def main(inf, outf):
     MAX = 1000
     fslst = []
     for i in itertools.count():
         if ispalindrome(i):
             squere = i * i
             print(MAX, squere, ispalindrome(squere))
             if squere > MAX:
                 break
             if ispalindrome(squere):
                 fslst.append(squere)
     for X, A, B in testcases(inf):
         cnt = 0
         for fs in fslst:
             if A <= fs <= B:
                 cnt += 1
         answer(outf, X, cnt)
 
 if __name__=="__main__":
     infname = sys.argv[1]
     outfname = os.path.splitext(infname)[0] + ".out"
     with open(infname, "r") as inf:
         with open(outfname, "w") as outf:
             main(inf, outf)
