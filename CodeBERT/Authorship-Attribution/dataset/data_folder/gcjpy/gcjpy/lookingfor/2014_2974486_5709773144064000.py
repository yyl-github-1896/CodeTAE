T = int(raw_input())
 
 def solve(C, F, X):
     best = x/2
     buildTime, speed = 0, 2
     while True:
         buildTime += C/speed
         if buildTime > best:
             break
         speed += F
         best = min(best, buildTime + X/speed)
     return best
 
 for z in xrange(T):
     c, f, x = map(float, raw_input().split())
     print "Case #%d: %.7f" % (z+1, solve(c, f, x))