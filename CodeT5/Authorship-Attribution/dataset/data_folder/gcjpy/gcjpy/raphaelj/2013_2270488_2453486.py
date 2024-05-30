t = int(input())
 
 def win(lines, player):
     for y in range(0, 4):
         count = 0
         for x in range(0, 4):
             if lines[y][x] in [player, 'T']:
                 count += 1
                 if count >= 4:
                     return True
             else:
                 break
 
     for x in range(0, 4):
         count = 0
         for y in range(0, 4):
             if lines[y][x] in [player, 'T']:
                 count += 1
                 if count >= 4:
                     return True
             else:
                 break
 
     count = 0
     for i in range(0, 4):
         if lines[i][i] in [player, 'T']:
             count += 1
             if count >= 4:
                 return True
 
     count = 0
     for i in range(0, 4):
         x = 3 - i
         if lines[i][x] in [player, 'T']:
             count += 1
             if count >= 4:
                 return True
 
     return False
 
 for i in range(0, t):
     lines = []
     for j in range(0, 4):
         lines.append(input())
     input()
 
     if win(lines, 'X'):
         sol = "X won"
     elif win(lines, 'O'):
         sol = "O won"
     else:
         void = False
         for y in range(0, 4):
             if any(c == '.' for c in lines[y]):
                 void = True
                 break
 
         if void:
             sol = "Game has not completed"
         else:
             sol = "Draw"
 
 
     print ("Case #"+str(i+1)+": "+sol)