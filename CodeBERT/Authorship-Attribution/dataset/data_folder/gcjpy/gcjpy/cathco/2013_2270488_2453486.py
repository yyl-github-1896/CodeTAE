def check(board):
   # Check rows.
   for i in range(4):
     row = board[i]
     if set(row) in [set(['X', 'T']), set(['X'])]:
       return 'X won'
     if set(row) in [set(['O', 'T']), set(['O'])]:
       return 'O won'
   
   # Check columns.
   for i in range(4):
     column = []
     for j in range(4):
       column.append(board[j][i])
     if set(column) in [set(['X', 'T']), set(['X'])]:
       return 'X won'
     if set(column) in [set(['O', 'T']), set(['O'])]:
       return 'O won'
   
   # Check diagonal top_left->bottom_right
   diag1 = [board[0][0], board[1][1], board[2][2], board[3][3]]
   if set(diag1) in [set(['X', 'T']), set(['X'])]:
       return 'X won'
   if set(diag1) in [set(['O', 'T']), set(['O'])]:
     return 'O won'
   
   # Check diagonal top_right->bottom_left
   diag2 = [board[3][0], board[2][1], board[1][2], board[0][3]]
   if set(diag2) in [set(['X', 'T']), set(['X'])]:
       return 'X won'
   if set(diag2) in [set(['O', 'T']), set(['O'])]:
     return 'O won'
   
   for i in range(4):
     for j in range(4):
       if board[i][j] == '.':
         return 'Game has not completed'
   return 'Draw'
 
 n = int(raw_input().strip())
 for i in range(n):
   board = []
   for j in range(4):
     line = raw_input()
     board.append([c for c in line])
   raw_input()
   print 'Case #%i: %s' % (i+1, check(board))
