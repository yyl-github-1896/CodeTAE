import sys
 
 
 def compute(r1, m1, r2, m2):
     valid1 = set(m1[r1 - 1])
     valid2 = set(m2[r2 - 1])
     valid = valid1 & valid2
     if len(valid) == 0:
         return 'Volunteer cheated!'
     if len(valid) > 1:
         return 'Bad magician!'
     return valid.pop()
 
 
 def parse_single():
     r = int(sys.stdin.readline().strip())
     m = []
     for i in xrange(4):
         m.append(map(int, sys.stdin.readline().strip().split()))
     return r, m
 
 def parse():
     r1, m1 = parse_single()
     r2, m2 = parse_single()
     return r1, m1, r2, m2
 
 
 if __name__ == "__main__":
     sys.setrecursionlimit(100000)
     T = int(sys.stdin.readline().strip())
     for i in xrange(T):
         data = parse()
         result = compute(*data)
         print "Case #%d: %s" % (i + 1, result)
