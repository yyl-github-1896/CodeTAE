import sys
 from bisect import bisect_left
 
 numCases = input()
 for case in range( 1, numCases + 1 ):
   N = input()
   Naomis = list( [float(x) for x in raw_input().split() ] )
   Kens = list( [float(x) for x in raw_input().split() ] )
   Naomis = sorted( Naomis )
   Kens = sorted( Kens )
 
   # sim optimal
   NaomisOptimal = Naomis[:]
   KensOptimal = Kens[:]
 
   KenScore = 0
   for i in xrange( 0, N ):
     Naomi = NaomisOptimal.pop()
     x = bisect_left( KensOptimal, Naomi )
     if x < len( KensOptimal ):
       KenScore += 1
       del KensOptimal[ x ]
     else:
       del KensOptimal[ 0 ]
 
   NScore = 0
   for i in xrange( 0, N ):
     Naomi = Naomis[0]
     del Naomis[0]
     x = bisect_left( Kens, Naomi )
     if x == 0:
       Kens.pop()
     else:
       NScore += 1
       del Kens[ 0 ]
 
     output = str( NScore ) + ' ' + str( N - KenScore )
   
   print 'Case #' + str( case ) + ': ' + str( output )
