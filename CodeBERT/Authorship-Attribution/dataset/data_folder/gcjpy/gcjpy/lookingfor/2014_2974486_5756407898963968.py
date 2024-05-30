T = int(raw_input())
 
 def readSq(n):
     res = []
     for i in xrange(n):
         res.append(set(map(int, raw_input().split())))
     return res
 
 def solve():
     a1 = int(raw_input())
     s1 = readSq(4)
     a2 = int(raw_input())
     s2 = readSq(4)
     ans = s1[a1-1] & s2[a2-1]
     if len(ans) == 0:
         return "Volunteer cheated!"
     if len(ans) > 1:
         return "Bad magician!"
     return str(list(ans)[0])
 
 for z in xrange(T):
     print "Case #%d: %s" % (z+1, solve())
