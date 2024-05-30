n_cases = input()
 
 for case in xrange(1, n_cases + 1):
     ins = map(int, raw_input().strip().split())
     n = ins[0]
     s = ins[1]
     p = ins[2]
     t = ins[3:]
 
     out = 0
     for x in t:
         if (x + 2) / 3 >= p:
             out += 1
         elif s and x > p and p - ((x - p) / 2) <= 2:
             out += 1
             s -= 1
             
     print "Case #%d: %s" % (case, out)
