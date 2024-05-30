import math
 import sys
 
 def ispal(n):
     s = str(n)
     return s == s[::-1]
 
 def ispalsq(n):
     sqrt = int(math.sqrt(n) + .01)
     if sqrt ** 2 != n:
         return False
     return ispal(n) and ispal(sqrt)
 
 def search(s, l, idx):
     if l % 2 == 0:
         m = s + s[::-1]
     else:
         m = s[:-1] + s[::-1]
     assert ispal(m)
     n = int(m) ** 2
     if not ispal(n):
         # print m, False
         return 0
     # print m, int(m)**2
 
     r = 1 if (a <= n <= b) else 0
     for i in xrange(idx, len(s)):
         s2 = list(s)
         s2[i] = str(int(s2[i])+1)
         s2 = ''.join(s2)
         r += search(s2, l, i)
     return r
 
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())
     for _t in xrange(t):
         a, b = map(int, f.readline().split())
 
         total = 0
         for l in xrange(1, 150):
             if 10 ** (l-1) > b:
                 break
             total += search("1" + "0" * ((l-1)/2), l, 0)
         print "Case #%d: %d" % (_t+1, total)
 
