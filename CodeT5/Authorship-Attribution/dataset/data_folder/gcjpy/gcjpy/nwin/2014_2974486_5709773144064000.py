def solve():
     c, f, x = map(float, raw_input().split())
     ans = 1e40
     cur = 0.0
     psp = 2.0
     while cur < ans + 1e-8:
         ans = min(ans, cur + x / psp)
         cur += c / psp
         psp += f
     return ans
 for t in xrange(int(raw_input())):
     print "Case #%d: %.7f" % (t + 1, solve())
