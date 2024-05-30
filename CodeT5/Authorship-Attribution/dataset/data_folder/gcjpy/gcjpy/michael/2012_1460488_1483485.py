def read_line():
     return raw_input().strip()
 
 def read_words():
     return read_line().split()
 
 def read_integer():
     return int( read_line() )
 
 def read_integers():
     return [ int( x ) for x in read_words() ]
 
 
 ciphers = 'y qee', 'ejp mysljylc kd kxveddknmc re jsicpdrysi', 'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd', 'de kr kd eoya kw aej tysr re ujdr lkgc jv'
 plaintexts = 'a zoo', 'our language is impossible to understand', 'there are twenty six factorial possibilities', 'so it is okay if you want to just give up'
 
 mapping = {}
 for cipher, plaintext in zip( ciphers, plaintexts ):
     for key, value in zip( cipher, plaintext ):
         mapping[ key.lower() ] = value.lower()
 mapping[ 'z' ] = 'q'
 
 T = read_integer()
 for t in range( T ):
     print 'Case #%i:' % ( t + 1 ), ''.join( mapping[ key.lower() ].upper() if key.isupper() else mapping[ key ] for key in read_line() )
