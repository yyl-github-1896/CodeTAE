from cStringIO import StringIO
 
 T = int(raw_input())
 
 def generate(R, C, a, sw):
     if sw:
         R, C = C, R
     res = [['*']*C for i in xrange(R)]
     for i in xrange(len(a)):
         for j in xrange(a[i]):
             if sw:
                 res[j][i] = '.'
             else:
                 res[i][j] = '.'
     res[0][0] = 'c'
     return str(res)[2:-2].replace(' ', '').replace("'",'').replace('[', '').replace('],','\n').replace(',', '')
 
 
 def solveEq(k, s, x1):
     if 2*(x1 + k - 2) > s or k*x1 < s:
         return None
     r = [0]*k
     r[0] = r[1] = x1
     s -= 2*x1
     for i in xrange(k-2, 0, -1):
         t = min(x1, s - 2*i + 2)
         r[k-i] = t
         s -= t
     return r
 
 def solve(R, C, M):
     S = R*C
     nm = S - M
     if R == 1 or C == 1:
         if R == 1:
             return '*'*M + '.'*(S-M-1) + 'c'
         else:
             return '*\n'*M + '.\n'*(S-M-1) + 'c'
     else:
         sw = False
         if R > C:
             R, C = C, R
             sw = True
         if nm == 2 or nm == 3 or nm == 5 or nm == 7 or (R == 2 and nm%2 == 1 and nm > 1):
             return "Impossible"
         if nm == 1:
             return generate(R, C, [1], sw)
         for k in xrange(2, R+1):
             for x1 in xrange(2, C+1):
                 r = solveEq(k, nm, x1)
                 if r != None:
                     return generate(R, C, r, sw)
         return "Something wrong"
 
 for z in xrange(T):
     c, f, x = map(int, raw_input().split())
     print "Case #%d:\n%s" % (z+1, solve(c, f, x))