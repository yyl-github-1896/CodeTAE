import sys
 
 def DrawMines( R, C, M, Flip, gridMines, sideMines, bottomMines ):
   x = []
   numSpaces = 0
   numMines = 0
 
   gridRows = max( R-2, 0 )
   gridCols = max( C-2, 0 )
 
   for r in xrange( 0, R ):
     x.append( [] )
     for c in xrange( 0, C ):
       x[ r ].append( '.' )
       numSpaces += 1
 
   if gridMines > 0:
     for r in xrange( 0, gridRows ):
       if numMines >= gridMines:
         break;
       for c in xrange( 0, gridCols ):
         x[ r ][ c ] = '*'
         numMines += 1
         numSpaces -= 1
         if numMines >= gridMines:
           break;
 
   for r in xrange( 0, R ):
     if sideMines <= 0:
       break
     for c in xrange( gridCols, C ):
       x[ r ][ c ] = '*'
       numMines += 1
       numSpaces -= 1
       sideMines -= 1
       if sideMines <= 0:
         break
 
   for c in xrange( 0, C ):
     if bottomMines <= 0:
       break
     for r in xrange( gridRows, R ):
       x[ r ][ c ] = '*'
       numMines += 1
       numSpaces -= 1
       bottomMines -= 1
       if bottomMines <= 0:
         break
     
   x[ R - 1][ C - 1 ] = 'c'
   
   if numMines != M and ( R * C ) - M != 1:
     print "ERROR!!!!!!!!!!!!!!!!!!!!!!!!"
     print ( R * C ) - M
 
 
   o = ""
 
   if Flip:
     for c in xrange( 0, C ):
       for r in xrange( 0, R ):
          o += x[ r ][ c ]
       o += '\n'
   else:
     for r in xrange( 0, R ):
       for c in xrange( 0, C ):
          o += x[ r ][ c ]
       o += '\n'
 
   return o[:-1] #strip the extra newline
 
 
 
 
 numCases = input()
 for case in xrange( 1, numCases + 1 ):
   R, C, M = [int(x) for x in raw_input().split()]
 
   Output = None
 
   Flip = C > R
   if Flip:
     temp = R
     R = C
     C = temp
 
   NonMines = ( R * C ) - M
   # Special cases first
   if ( NonMines == 0 ):
     Output = "Impossible"
   elif ( C == 1 ):
     gridMines = 0
     extraMines = M - gridMines
     Output = DrawMines( R, C, M, Flip, gridMines, extraMines, 0 )
   elif ( NonMines == 2 or  NonMines == 3 ):
     Output = "Impossible"
   else:
     maxGridCols = max( 0, C - 2 )
     maxGridRows = max( 0, R - 2 )
     gridMines = min( M, maxGridCols * maxGridRows )
     extraMines = M - gridMines
     extraPairs = ( extraMines + 1 ) / 2
     extraPairsSide = max( min( extraPairs, maxGridRows - 1 ), 0 )
     extraPairsBottom = max( min( extraPairs - extraPairsSide, maxGridCols - 1 ), 0 )
     safeExtraPairs = extraPairsSide + extraPairsBottom
     blockingPairsSide = max( min( extraPairs - safeExtraPairs, 1 ), 0 )
     blockingPairsBottom = max( min( extraPairs - blockingPairsSide - safeExtraPairs, 1 ), 0 )
     blockingPairs = blockingPairsSide + blockingPairsBottom
     totalPairs = safeExtraPairs + blockingPairs
 
     
     if ( gridMines > 0 and extraMines % 2 != 0 and blockingPairs == 0 ):
       extraMines += 1
       gridMines -= 1
 
     if ( NonMines == 1 ):
       if extraMines % 2 != 0:
         extraMines += 1
       blockingPairsSide += 1
       blockingPairsBottom += 1
     
     if extraMines % 2 == 0:
       sideMines = 2 * ( extraPairsSide + blockingPairsSide )
       bottomMines = 2 * ( extraPairsBottom + blockingPairsBottom )
       Output = DrawMines( R, C, M, Flip, gridMines, sideMines, bottomMines )
     else:
       Output = "Impossible"
 
   output = "\n" + Output
   print 'Case #' + str( case ) + ': ' + str( output )
