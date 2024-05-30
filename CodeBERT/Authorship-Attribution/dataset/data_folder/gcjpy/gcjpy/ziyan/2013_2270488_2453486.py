
 import sys
 
 def process():
     empty = 0
     board = [['.', '.', '.', '.'] for i in range(4)]
     for r in range(4):
         row = sys.stdin.readline()
         for c in range(4):
             board[r][c] = row[c]
             if row[c] == '.': empty = empty + 1
     sys.stdin.readline()
 
     # print board
 
     # check rows
     for r in range(4):
         x = 0
         o = 0
         for c in range(4):
             if board[r][c] == 'X':
                 x = x + 1
             if board[r][c] == 'O':
                 o = o + 1
             if board[r][c] == 'T':
                 x = x + 1
                 o = o + 1
         if x == 4: return "X won"
         if o == 4: return "O won"
 
     for c in range(4):
         x = 0
         o = 0
         for r in range(4):
             if board[r][c] == 'X':
                 x = x + 1
             if board[r][c] == 'O':
                 o = o + 1
             if board[r][c] == 'T':
                 x = x + 1
                 o = o + 1
         if x == 4: return "X won"
         if o == 4: return "O won"
 
     x = 0
     o = 0
     for c in range(4):
         r = c
         if board[r][c] == 'X':
             x = x + 1
         if board[r][c] == 'O':
             o = o + 1
         if board[r][c] == 'T':
             x = x + 1
             o = o + 1
 
     if x == 4: return "X won"
     if o == 4: return "O won"
 
     x = 0
     o = 0
     for c in range(4):
         r = 3 - c
         if board[r][c] == 'X':
             x = x + 1
         if board[r][c] == 'O':
             o = o + 1
         if board[r][c] == 'T':
             x = x + 1
             o = o + 1
 
     if x == 4: return "X won"
     if o == 4: return "O won"
 
     if empty == 0: return "Draw"
 
     return "Game has not completed"
 
         
 
 def main():
 
     count = int(sys.stdin.readline())
     for index in range(count):
         result = process()
         print "Case #%d: %s" % (index + 1, result)
 
 if __name__ == '__main__':
     main()
