def read_line():
     return raw_input().strip()
 
 def read_words():
     return read_line().split()
 
 def read_integer():
     return int( read_line() )
 
 def read_integers():
     return [ int( x ) for x in read_words() ]
 
 T = read_integer()
 for t in range( T ):
     print 'Case #%i:' % ( t + 1 ),
     A, B = read_integers()
     length = len( str( A ) )
     pairs = set()
     for n in range( A, B ):
         digits = str( n )
         for start in range( 1, length ):
             m = int( digits[ start : ] + digits[ : start ] )
             if n < m <= B:
                 pairs.add( ( n, m ) )
     print len( pairs )
