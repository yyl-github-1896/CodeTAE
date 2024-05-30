T = int(raw_input())
 
 def solve(a, b):
     n = len(a)
     a.sort()
     b.sort()
     i = j = m = M = 0
     while i < n:
         if a[i] > b[j]:
             M += 1
             i += 1
             j += 1
         else:
             i += 1
     i = j = 0
     while j < n:
         if b[j] > a[i]:
             m += 1
             i += 1
             j += 1
         else:
             j += 1
     return str(M) + " " + str(n-m)
 
 for z in xrange(T):
     n = int(raw_input())
     a = map(float, raw_input().split())
     b = map(float, raw_input().split())
     print "Case #%d: %s" % (z+1, solve(a, b))