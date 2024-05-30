filename = "A-small-attempt0 (3).in"
 outputname = filename + "out.txt"
 
 inFile = open(filename, 'r')
 outFile = open(outputname, 'w')
 
 
 
 
 
 def evalGame(lines):
     board = []
     gameOver = True
     
     for line in lines:
         bline = []
         for i in range(len(line)):
             if line[i] == 'X':
                 bline += [1]
             elif line[i] == 'O':
                 bline += [2]
             elif line[i] == 'T':
                 bline += [3]
             elif line[i] == '.':
                 gameOver = False
                 bline += [0]
         board += [bline]
 
     # Check down
     for i in range(1):
         for j in range(4):
             startTile = board[i][j]
             if startTile == 3 or startTile == 0:
                 continue
             winner = True
             for k in range(1,4):
                 if board[i+k][j] not in [startTile, 3]:
                     winner = False
                     break
             if winner:
                 return startTile
 
     # Check right
     for i in range(4):
         for j in range(1):
             startTile = board[i][j]
             if startTile == 3 or startTile == 0:
                 continue
             winner = True
             for k in range(1,4):
                 if board[i][j+k] not in [startTile, 3]:
                     winner = False
                     break
             if winner:
                 return startTile
 
     # Check up
     for i in range(3,4):
         for j in range(4):
             startTile = board[i][j]
             if startTile == 3 or startTile == 0:
                 continue
             winner = True
             for k in range(1,4):
                 if board[i-k][j] not in [startTile, 3]:
                     winner = False
                     break
             if winner:
                 return startTile
 
     # Check left
     for i in range(4):
         for j in range(3,4):
             startTile = board[i][j]
             if startTile == 3 or startTile == 0:
                 continue
             winner = True
             for k in range(1,4):
                 if board[i][j-k] not in [startTile, 3]:
                     winner = False
                     break
             if winner:
                 return startTile
     
      # Check down right
     startTile = board[0][0]
     if startTile != 3 and startTile != 0:
         winner = True
         for k in range(1,4):
             if board[k][k] not in [startTile, 3]:
                 winner = False
                 break
         if winner:
             return startTile
 
      # Check up right
     startTile = board[3][0]
     if startTile != 3 and startTile != 0:
         winner = True
         for k in range(1,4):
             if board[3-k][k] not in [startTile, 3]:
                 winner = False
                 break
         if winner:
             return startTile
 
      # Check up left
     startTile = board[3][3]
     if startTile != 3 and startTile != 0:
         winner = True
         for k in range(1,4):
             if board[3-k][3-k] not in [startTile, 3]:
                 winner = False
                 break
         if winner:
             return startTile
 
      # Check down left
     startTile = board[0][3]
     if startTile != 3 and startTile != 0:
         winner = True
         for k in range(1,4):
             if board[k][3-k] not in [startTile, 3]:
                 winner = False
                 break
         if winner:
             return startTile
 
 
     if gameOver:
         return 0
 
     else:
         return -1
     
                       
 
 
 
 
 
 def resultToString(result):
     if result == 0:
         return "Draw"
     elif result == 1:
         return "X won"
     elif result == 2:
         return "O won"
     else:
         return "Game has not completed"
 
 
 numCases = int(inFile.readline())
 
 for i in range(numCases):
     lines = []
     for j in range(4):
         lines += [inFile.readline().strip()]
 
     result = evalGame(lines)
 
     print "Case #" + str(i+1) + ": " + resultToString(result)
     outFile.write("Case #" + str(i+1) + ": " + resultToString(result) + '\n')
     
     if i < numCases -1:
         inFile.readline()
 
 inFile.close()
 outFile.close()
