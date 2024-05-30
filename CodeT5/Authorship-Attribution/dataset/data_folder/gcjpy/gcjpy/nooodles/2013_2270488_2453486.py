def Winner( M ):
     for i in range(4):          # Check rows
         nX = 0;     nO = 0;     
         for j in range(4):
             if M[i][j] == 'X':
                 nX += 1;
             if M[i][j] == 'O':
                 nO += 1;
             if M[i][j] == 'T':
                 nX += 1;
                 nO += 1;
         if nX == 4:
             return 'X';
         if nO == 4:
             return 'O';
         
     for j in range(4):          # Check columns
         nX = 0;     nO = 0;     
         for i in range(4):
             if M[i][j] == 'X':
                 nX += 1;
             if M[i][j] == 'O':
                 nO += 1;
             if M[i][j] == 'T':
                 nX += 1;
                 nO += 1;
         if nX == 4:
             return 'X';
         if nO == 4:
             return 'O';
 
     if (M[0][0] in ['X','T']) and (M[1][1] in ['X','T']) and (M[2][2] in ['X','T']) and (M[3][3] in ['X','T']):
         return 'X';
     if (M[0][3] in ['X','T']) and (M[1][2] in ['X','T']) and (M[2][1] in ['X','T']) and (M[3][0] in ['X','T']):
         return 'X';
     if (M[0][0] in ['O','T']) and (M[1][1] in ['O','T']) and (M[2][2] in ['O','T']) and (M[3][3] in ['O','T']):
         return 'O';           
     if (M[0][3] in ['O','T']) and (M[1][2] in ['O','T']) and (M[2][1] in ['O','T']) and (M[3][0] in ['O','T']):
         return 'O';
 
     return 'D';            
 
 
 T = int(raw_input());
 for q in range(T):
     if q != 0:
         raw_input();
     Map = [];
     Dot = False;
     for i in range(4):
         Map.append( raw_input() );
         if '.' in Map[-1]:
             Dot = True;
 
     ANS = Winner(Map);
 #    print ANS
     if ANS == 'X':
         print "Case #%d: X won" %(q+1)
     if ANS == 'O':
         print "Case #%d: O won" %(q+1)
     if ANS == 'D':
         if Dot:
             print "Case #%d: Game has not completed" %(q+1)
         else:
             print "Case #%d: Draw " % (q+1)
 
