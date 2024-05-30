import sys
 
 def read_line():
     return sys.stdin.readline().rstrip( '\n' )
 
 def read_integer():
     return int( read_line() )
 
 def read_integers():
     return [ int( x ) for x in read_line().split() ]
 
 def read_string():
     return read_line().strip()
 
 def read_strings():
     return read_line().split()
 
 def input_string_stack():
     data = []
     for line in sys.stdin.readlines():
         data.extend( line.split() )
     data.reverse()
     return data
 
 def input_integer_stack():
     return [ int( x ) for x in read_string_stack() ]
 
 class memoized( object ):
    def __init__( self, function ):
       self.function = function
       self.cache = {}
    def __call__( self, *arguments ):
       try:
          return self.cache[ arguments ]
       except KeyError:
          value = self.function( *arguments )
          self.cache[ arguments ] = value
          return value
 
 T = read_integer()
 for t in range( T ):
     row = read_integer()
     candidates = set( [ read_integers() for index in range( 4 ) ][ row - 1 ] )
     row = read_integer()
     candidates &= set( [ read_integers() for index in range( 4 ) ][ row - 1 ] )
     print 'Case #%i:' % ( t + 1 ), candidates.pop() if len( candidates ) == 1 else 'Bad magician!' if len( candidates ) > 1 else 'Volunteer cheated!'
