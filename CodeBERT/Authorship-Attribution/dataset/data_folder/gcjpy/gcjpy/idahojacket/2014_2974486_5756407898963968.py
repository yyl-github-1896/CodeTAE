import sys
 
 numCases = input()
 for case in range( 1, numCases + 1 ):
   row1 = input()
   grid1 = []
   for i in range( 0, 4 ):
     grid1.append( raw_input().split() )
 
   cards = grid1[ row1 - 1 ]
 
   row2 = input()
   grid2 = []
   for i in range( 0, 4 ):
     grid2.append( raw_input().split() )
 
   bad = True
       
   cards2 = grid2[ row2 - 1 ]
 
   numPossibleAnswers = 0
   for card in cards:
     for card2 in cards2:
       if ( card == card2 ):
         if numPossibleAnswers == 0:
           output = card
         numPossibleAnswers += 1
         break
 
   if numPossibleAnswers == 0:
     output = "Volunteer cheated!"
   elif numPossibleAnswers > 1:
     output = "Bad magician!"
 
   print 'Case #' + str( case ) + ': ' + str( output )
