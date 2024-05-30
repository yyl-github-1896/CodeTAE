def up_down(board, height, y, x):
   # Move up from (x, y).
   above = y - 1
   while above >= 0:
     if board[above][x] > board[y][x]: 
       return False
     above -= 1
   # Move down from (x, y).
   below = y + 1
   while below < height:
     if board[below][x] > board[y][x]: 
       return False
     below += 1
   return True
   
 def left_right(board, width, y, x):
   # Move left from (x, y).
   before = x - 1
   while before >= 0:
     if board[y][before] > board[y][x]: 
       return False
     before -= 1
   # Move right from (x, y).
   after = y + 1
   while after < width:
     if board[y][after] > board[y][x]: 
       return False
     after += 1
   return True
   
 def check(board, height, width):
   if height == 1 or width == 1:
     return 'YES'
   for i in range(height):
     for j in range(width):
       if (not up_down(board, height, i, j)) and (not left_right(board, width, i, j)):
         return 'NO'
   return 'YES'
 
 n = int(raw_input().strip())
 for i in range(n):
   height, width = map(int,  raw_input().strip().split(' '))
   board = []
   for _ in range(height):
     row = map(int, raw_input().strip().split(' '))
     board.append(row)
   print 'Case #%i: %s' % (i+1, check(board, height, width))
