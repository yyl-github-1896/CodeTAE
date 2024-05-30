import sys
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     T = int(f.readline())
     for _T in xrange(T):
         C, F, X = map(float, f.readline().split())
 
         cps = 2.0
         t = 0.0
         best_t = X / cps
 
         while True:
             t += C / cps
             if t >= best_t:
                 break
 
             cps += F
             best_t = min(best_t, t + X / cps)
 
         print "Case #%d: %.7f" % (_T+1, best_t)
