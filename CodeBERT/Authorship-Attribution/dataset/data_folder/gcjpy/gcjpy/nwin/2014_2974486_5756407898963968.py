def solve():
     r1 = int(raw_input())
     a1 = [map(int, raw_input().split()) for i in xrange(4)]
     r2 = int(raw_input())
     a2 = [map(int, raw_input().split()) for i in xrange(4)]
     ans = -1
     for i in xrange(1, 17):
         if i in a1[r1-1] and i in a2[r2-1]:
             if ans != -1:
                 return "Bad magician!"
             ans = i
     if ans == -1:
         return "Volunteer cheated!"
     return ans
 for t in xrange(int(raw_input())):
     print "Case #%d:" % (t + 1), solve()
