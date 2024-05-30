def get_a(r, c, f='.'):
     A = []
     for i in xrange(r):
         A.append([f] * c)
     return A
 
 
 def apply(A, r, c, B):
     for i, b in enumerate(B):
         for j, v in enumerate(b):
             A[r + i][c + j] = v
 
 
 def draw(A):
     if A is None:
         return '\nImpossible'
     res = ['']
     for a in A:
         res.append(''.join(a))
     return '\n'.join(res)
 
 
 def trans(A):
     if not A:
         return None
     B = get_a(len(A[0]), len(A))
     for i, a in enumerate(A):
         for j, v in enumerate(a):
             B[j][i] = v
     return B
 
 
 def check(A, m, r, c):
     if A is None:
         return True
     cnts = {'c': 0, '*': 0, '.': 0}
     #print draw(A)
     #print
 
     assert len(A) == r
     for i in xrange(r):
         assert len(A[i]) == c
         for j in xrange(c):
             cnts[A[i][j]] += 1
     #print m, r, c, "=>", cnts
     assert cnts['*'] == m
     assert cnts['c'] == 1
     assert cnts['.'] == r * c - m - 1
 
 
 def CASE(IN):
     def rstr():
         return IN.readline().strip()
 
     def rint():
         return int(rstr())
 
     def rints():
         return map(int, rstr().split())
     r, c, m = rints()
     A = solve(m, r, c)
     if A:
         A[-1][-1] = 'c'
     check(A, m, r, c)
     return draw(A)
 
 
 def solve(m, r, c):
     if r > c:
         return trans(solve(m, c, r))
     assert r <= c
     assert m != r * c
     e = r * c - m
     # we click always in the right bottom corner
     if e == 1:
         A = get_a(r, c, '*')
         return A
     if r == 1:
         A = get_a(1, c, '.')
         for i in xrange(m):
             A[0][i] = '*'
         return A
     if r == 2:
         if e == 2 or e % 2 == 1:
             return None
         A = get_a(2, c, '.')
         assert m % 2 == 0
         for i in xrange(m / 2):
             A[0][i] = A[1][i] = '*'
         return A
     assert r >= 3
     A = get_a(r, c, '*')
     if e in (2, 3, 5, 7):
         return None
     E = [c] * (e / c) + ([e % c] if e % c else [])
     if sum(E) < e:
         E.append(e % c)
         assert sum(E) == e
     if len(E) == 1:
         E = [e / 2] * 2
         if sum(E) < e:
             e.append(1)
     if E[0] != E[1]:
         s = sum(E[:2])
         E[0] = E[1] = s / 2
         if sum(E[:2]) != s:
             assert len(E) == 2
             E.append(1)
     if E[-1] == 1:
         if len(E) > 3:
             E[-2] -= 1
             E[-1] += 1
         else:
             E[0] -= 1
             E[1] -= 1
             E[2] += 2
     for i in xrange(len(E)):
         for j in xrange(E[i]):
             A[-i - 1][-j - 1] = '.'
     return A
 
 
 def RUN(IN, OUT):
     t = int(IN.readline().strip())
     for i in xrange(1, t + 1):
         OUT.write("Case #%i: %s\n" % (i, CASE(IN)))
 
 if __name__ == "__main__":
     import sys
     RUN(sys.stdin, sys.stdout)
