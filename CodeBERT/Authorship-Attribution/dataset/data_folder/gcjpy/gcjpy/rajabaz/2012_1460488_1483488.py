def num_rotations(n, A, B):
     # I'm sure there's a better way to do this
     # but this works fast enough so who cares
     s = str(n)
     a = set()
     for i in range(len(s)):
         rotated = s[i:] + s[:i]
         r = int(rotated)
         if rotated[0] != '0' and A <= r <= B:
             a.add(rotated)
     return len(a) -1
 
 def solve(A,B):
     t  = 0
     for i in range(A, B+1):
         t += num_rotations(i, A, B)
     if t % 2 != 0:
         print "WTF", A, B, t
     return t//2
 
 if __name__ == "__main__":
     T = int(raw_input())
     for i in range(1, T+1):
         A,B = map(int, raw_input().strip().split())
         print "Case #%d: %d" % (i, solve(A,B))
