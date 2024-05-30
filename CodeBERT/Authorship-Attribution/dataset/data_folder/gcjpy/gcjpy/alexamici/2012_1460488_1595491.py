"""Usage:
     X.py < X.in > X.out
 """
 
 import sys
 
 
 class Solver(object):
     cache = {}
 
     def __init__(self, infile, testcase):
         self.testcase = testcase
         self.P = P = map(int, infile.next().split())
 
     def init_cache(self):
         if 'main' in self.cache:
             return
         #self.cache['main'] = res
 
     def solve(self):
 
         N, S, p = self.P[:3]
         G = sorted(self.P[3:], reverse=True)
 
         r = 0
         s = 0
         for g in G:
             if g >= 3 * p - 2 and g >= p:
                 r += 1
             elif g >= 3 * p - 4 and g >= p:
                 if s == S:
                     break
                 r += 1
                 s += 1
 
         return r
 
 
 def main():
     T = int(sys.stdin.next())
     for t in xrange(T):
         sys.stdout.write('Case #%s: %s\n' % (t + 1, Solver(sys.stdin, t).solve()))
 
 
 if __name__ == '__main__':
     main()
