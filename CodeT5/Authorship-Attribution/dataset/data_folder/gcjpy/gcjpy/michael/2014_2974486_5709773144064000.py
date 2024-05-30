import sys
 
 def read_line():
     return sys.stdin.readline().rstrip( '\n' )
 
 def read_integer():
     return int( read_line() )
 
 def read_float():
     return float( read_line() )
 
 def read_floats():
     return [ float( x ) for x in read_line().split() ]
 
 T = read_integer()
 for t in range( T ):
     C, F, X = read_floats()
     rate = 2
     cookies = 0
     s = 0
     while True:
         t1 = X/rate
         t2 = C/rate + X/( rate + F )
         if t1 < t2:
             s += t1
             break
         s += C/rate
         rate += F
     print 'Case #%i: %.7f' % ( t + 1, s )
