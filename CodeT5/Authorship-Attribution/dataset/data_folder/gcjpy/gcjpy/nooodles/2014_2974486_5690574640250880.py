def Trivial(R,C,char):
 #    print
     for i in range(R):
         Ans = '';
         for j in range(C):
             if (i==j==0):
                 Ans += 'c';
             else:
                 Ans += char;
         print Ans;
 
 
 def Draw1(R,C,Blank):
 #    print
     Ans = "c";
     for i in range(Blank-1):
         Ans += '.';
     for i in range(R*C-Blank):
         Ans += '*';
     if (R == 1):
         print Ans;        
         return;
     if (C == 1):
         for i in range(len(Ans)):
             print Ans[i];
 
 def Draw2(R,C,Blank):
     if (Blank%2 != 0) or (Blank == 2):
         print "Impossible";
         return;
     Row1 = '.'*(Blank/2) + '*'*(Mine/2);
     Row0 = 'c' + Row1[1:];
     if R==2:
         print Row0;
         print Row1;
     else:
         for i in range(len(Row0)):
             print Row0[i]+Row1[i];
     return;
 
 
 def Generate(R, C, Blank):
     TODO = Blank;
     Spaces = [0]*R;
     if TODO <= 2*C:
         if TODO%2 == 0:
             Spaces[0] = TODO/2;
             Spaces[1] = TODO-Spaces[0];
         else:
             if (TODO == 7):
                 Spaces[0] = 3;
                 Spaces[1] = 2;
                 Spaces[2] = 2;
             else:
                 Spaces[0] = (TODO-3)/2;
                 Spaces[1] = (TODO-3)/2;
                 Spaces[2] = 3;
     else:
         row = 0;
         if (TODO >= 2*C+2):
             Spaces[0] = C;
             Spaces[1] = C;
             TODO -= 2*C;
             row = 2;
             
         while TODO > C+1:
             if (TODO == 2*C+1) and (C != 3):
                 Spaces[row] = C-1;
                 Spaces[row+1] = C-1;
                 Spaces[row+2] = 3;
                 TODO = 0;
             else:
                 Spaces[row] = C;
                 TODO -= C;
                 row += 1;
         if (TODO == C+1):
             Spaces[row] += C-1;
             Spaces[row+1] = 2;
             TODO = 0;
         Spaces[row] += TODO;
 
     for r in range(R):
         Ans = '.'*Spaces[r] + '*'*(C-Spaces[r]);
         if r == 0:
             Ans = 'c'+Ans[1:];
         print Ans;
 
 
 def Solve(R, C, M):
     Blank = R*C-M;
     if Blank == 0:
         print "Impossible";
         return;
 
     if (Blank == 1):
         Trivial(R,C,'*');
         return
     if (Blank == R*C):
         Trivial(R,C,'.');
         return
 
     if (R == 1) or (C == 1):
           Draw1(R,C,Blank);
           return
 
     if (R-2)*(C-2) == 0:
         Draw2(R,C,Blank);
         return
 
     if Blank in [2,3,5,7]:
         print "Impossible";
         return;
     
     if (R >= 3) and (C >= 3):
         Generate(R, C, Blank);
 
     return;
 
 
 T = int(raw_input());
 for q in range(T):
     [Row,Col,Mine] = map(int, raw_input().split());
 
     Blanks = Row*Col - Mine;
     
     print "Case #%d:" % (q+1)
 #    print str(Row)+'x'+str(Col)+' with '+str(Mine)+' mines ('+str(Blanks)+' gaps)'
     Solve(Row, Col, Mine);
     
         
