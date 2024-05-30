import sys
 
 numCases = input()
 for case in range( 1, numCases + 1 ):
   C, F, X = raw_input().split()
   C = float(C)
   F = float(F)
   X = float(X)
   time = 0.0
   rate = 2.0
   
   while ( True ):
     timeToFinish = X / rate
     timeToFarm   = C / rate
     farmPayoffTime = C / F
 
     if timeToFinish < ( timeToFarm + farmPayoffTime ):
       time += timeToFinish
       break
     else:
       time += timeToFarm
       rate += F
 
 
   output = '{0:0.15f}'.format( time )
 
   print 'Case #' + str( case ) + ': ' + str( output )
