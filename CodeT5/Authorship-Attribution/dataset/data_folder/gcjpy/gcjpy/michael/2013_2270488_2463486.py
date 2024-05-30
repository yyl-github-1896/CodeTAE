from math import *
 
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
     A, B = read_integers()
     A_root = int( ceil( sqrt( A ) ) )
     B_root = int( floor( sqrt( B ) ) )
     count = 0
     for root in range( A_root, B_root + 1 ):
         word = str( root )
         if word == word[ : : -1 ]:
             word = str( root*root )
             if word == word[ : : -1 ]:
                 count += 1
     print 'Case #%i:' % ( t + 1 ), count
