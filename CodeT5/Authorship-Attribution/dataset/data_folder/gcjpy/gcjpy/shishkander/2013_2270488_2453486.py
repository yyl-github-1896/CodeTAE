def test_win(M, c):
     N = len(M)
     def yielder():
         for row in M:
             yield row, 'row'
         for i in xrange(N):
             yield [row[i] for row in M], 'col'
         yield [M[i][i] for i in xrange(N)], 'd1'
         yield [M[i][N-i-1] for i in xrange(N)], 'd2'
     for lst, typ in yielder():
         if all(l == c or l == 'T' for l in lst):
             #print "won at %s %s" % (lst, typ)
             return True
     return False
 
 def CASE(IN):
     def rstr(): return IN.readline().strip()
     def rint(): return int(rstr())
     def rints(): return map(int, rstr().split())
     M = [rstr() for i in xrange(4)]
     rstr()
     #print M
     if test_win(M, 'X'):
         return 'X won'
     if test_win(M, 'O'):
         return 'O won'
     if any('.' in row for row in M):
         return 'Game has not completed'
     return 'Draw'
 
 def RUN(IN, OUT):
     t = int(IN.readline().strip())
     for i in xrange(1,t+1):
         OUT.write("Case #%i: %s\n" % (i, CASE(IN)))
 
 if __name__ == "__main__":
     import sys
     RUN(sys.stdin, sys.stdout)
