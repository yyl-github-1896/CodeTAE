import sys
 
 def get_winner( row ):
 	if row.count( 'X' ) + row.count( 'T' )  == size:
 		return 'X won'
 	if row.count( 'O' ) + row.count( 'T' )  == size:
 		return 'O won'
 	return 'Draw'
 	
 
 numCases = input()
 for case in range( 1, numCases + 1 ):
 	size = 4
 	board = {}
 	full = True
 	winner = 'Draw'
 	
 	for row in range( 0, size ):
 		row_raw = raw_input()
 		board[row] = row_raw
 		if '.' in row_raw:
 			full = False
 
 		if winner == 'Draw':
 			winner = get_winner( row_raw )
 	
 	raw_input()
 
 	if winner == 'Draw':
 		for col in range( 0, size ):
 			row_new = ''
 			for row in range( 0, size ):
 				row_new += board[row][col]
 			winner = get_winner( row_new )
 			if winner != 'Draw':
 				break
 
 	if winner == 'Draw':
 		row_new = ''
 		for z in range( 0, size ):
 			row_new += board[z][z]
 		winner = get_winner( row_new )
 		if winner == 'Draw':
 			row_new = ''
 			for z in range( 0, size ):
 				row_new += board[z][size - z - 1]
 			winner = get_winner( row_new )
 		
 
 	if winner == 'Draw' and not full:
 		winner = 'Game has not completed'
 
 	print 'Case #' + str( case ) + ': ' + winner
