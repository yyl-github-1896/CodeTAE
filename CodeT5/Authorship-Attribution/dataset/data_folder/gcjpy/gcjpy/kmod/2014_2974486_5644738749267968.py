import sys
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     T = int(f.readline())
     for _T in xrange(T):
         N = int(f.readline())
         naomi = map(float, f.readline().split())
         ken = map(float, f.readline().split())
         assert len(ken) == len(naomi) == N
 
         naomi = [(w, 1) for w in naomi]
         ken = [(w, 0) for w in ken]
 
         blocks = ken + naomi
         blocks.sort(reverse=True)
         blocks = [p[1] for p in blocks]
         # print blocks
 
         honest = 0
         adv = 0
         for b in blocks:
             if b == 1:
                 adv += 1
                 honest = max(honest, adv)
             else:
                 adv -= 1
 
         deceitful = 0
         kept = 0
         for b in blocks:
             if b == 1:
                 kept += 1
             else:
                 if kept:
                     kept -= 1
                     deceitful += 1
         print "Case #%d: %d %d" % (_T+1, deceitful, honest)
