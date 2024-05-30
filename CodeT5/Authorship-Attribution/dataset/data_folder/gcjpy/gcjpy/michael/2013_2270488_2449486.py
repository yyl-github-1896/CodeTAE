from numpy import *
 
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
     N, M = read_integers()
     lawn = array( [ read_integers() for n in range( N ) ] )
     valid = zeros( lawn.shape, bool )
     for row in range( N ):
         valid[ row ][ lawn[ row ] == amax( lawn[ row ] ) ] = True
     for column in range( M ):
         valid[ :, column ][ lawn[ :, column ] == amax( lawn[ :, column ] ) ] = 1
     print 'Case #%i:' % ( t + 1 ), 'YES' if all( valid ) else 'NO'
