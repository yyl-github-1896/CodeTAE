def max_of_triplets(n):
     a = n//3
     if (n % 3) == 0:
         if a == 0 : return (0,0)
         return (a, a+1)
     if (n % 3) == 1:
         return (a+1, a+1)
     if a == 9: return (10, 10)
     return (a+1, a+2)
 
 def solve(scores, S, p):
     t = 0
     for s in scores:
         a,b = max_of_triplets(s)
         if a >= p:
             t += 1
         elif b >= p and S > 0:
             t += 1
             S -= 1
     return t
 
 if __name__ == "__main__":
     T = int(raw_input())
     for i in range(1, T+1):
         nums = map(int, raw_input().strip().split())
         N = nums[0]
         S = nums[1]
         p = nums[2]
         scores = nums[3:]
         if len(scores) != N:
             #sanity check
             print "WTF", i
         print "Case #%d: %d" % (i, solve(scores, S, p))
     
