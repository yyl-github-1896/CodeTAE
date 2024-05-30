import sys
 
 def solve(a, b):
     count = 0
     for n in xrange(a, b):
         s = str(n)
         for i in xrange(len(s)):
             m = int(s[i:] + s[:i])
             if n < m <= b:
                 count += 1
     return count
 
 if __name__ == '__main__':
     with open(sys.argv[1], 'rU') as fin, open(sys.argv[2], 'w') as fout:
         T = int(fin.readline())
         for case in xrange(1, T+1):
             a, b = map(int, fin.readline().split())
             print >> fout, "Case #{0}: {1}".format(case, solve(a, b))
