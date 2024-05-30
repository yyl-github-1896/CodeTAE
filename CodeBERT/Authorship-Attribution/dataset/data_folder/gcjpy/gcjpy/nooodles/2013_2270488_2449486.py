T = int(raw_input());
 for q in range(T):
     [H,W] = map(int, raw_input().split());
     Lawn = [];
     MRow = [0]*H;
     MCol = [0]*W;
     for i in range(H):
         Lawn.append( map(int, raw_input().split()) );
         MRow[i] = max(Lawn[-1]);
         for j in range(W):
             MCol[j] = max(MCol[j], Lawn[-1][j]);
 
     Valid = True;
     for i in range(H):
         for j in range(W):
             if Lawn[i][j] not in [MRow[i], MCol[j]]:
                 Valid = False;
                 break;
     
 
     if Valid:
         print "Case #%d: YES" %(q+1);
     else:
         print "Case #%d: NO" %(q+1);        
