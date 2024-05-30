import math
 import sys
 
 
 def compute(C, F, X):
     k = int(math.floor(X / C - 2.0 / F))
     if k <= 0:
         return X / 2
     total = 0.0
     for i in xrange(k):
         total += 1.0 / (2.0 + i * F)
     return C * total + X / (2.0 + k * F)
 
 
 def parse():
     C, F, X = map(float, sys.stdin.readline().strip().split())
     return C, F, X
 
 
 if __name__ == "__main__":
     sys.setrecursionlimit(100000)
     T = int(sys.stdin.readline().strip())
     for i in xrange(T):
         data = parse()
         result = compute(*data)
         print "Case #%d: %0.7f" % (i + 1, result)
