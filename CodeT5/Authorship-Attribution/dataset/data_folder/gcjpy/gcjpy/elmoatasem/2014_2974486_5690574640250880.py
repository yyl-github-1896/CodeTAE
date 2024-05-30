'''
 Created on Apr 12, 2014
 
 @author: mostasem
 '''
 
 import math
 def getFloorRoots(m):
     r1 = -1 + math.sqrt(1 + (8 * m))/2
     r2 = -1 - math.sqrt(1 + (8 * m))/2
     return int(math.floor(r1))
     
 def boardHasZero(R,C,M):
     if(R > 1 and C > 1):
         S = M/C
         Sr = M % C
         print S,Sr
         return R >= S+3 or (R == S+2 and ((Sr % 2) == 0 or (((C + Sr) % 3 == 0) and (2*C >= (C + Sr + 4))))) or (R == S+1  and (C + Sr) % 2 == 0 and (2*C >= (C + Sr + 4)))  #M <= ((R*C) - 4)
     else :
         return M <= ((R*C) - 2)
 
 
 def generateMineSweeperCase(R,C,M):
 
     board = ""
 
     if( R > 1 and C > 1 ): # generate special
         S = M/C
         Sr = M % C
         print S,Sr
         if(S): # all rows of *
             board +="\n"
             if(R >= S+3 or (R == S+2 and Sr % 2 == 0)):
                 board += (S - 1) * ((C*"*") + "\n")
             else:
                 board += (S - 2) * ((C*"*") + "\n")
             board +=  ((C*"*"))
             
         if(R >= S+3):
             if(Sr):
                 board +="\n"
                 board += ((Sr *"*") + ((C - Sr) *"."))
             Rm = R - (S + 1)
             if(Rm):
                 board +="\n"
                 board += (Rm - 1) * ((C*".") + "\n")
                 board +=  ((C*"."))
                 
         elif(R == S + 2):
             Sm = 0
             if(Sr % 2 == 0):
                 board +="\n"
                 board += (((Sr / 2) *"*") + ((C - (Sr / 2)) *".") +"\n")
                 board += ((Sr / 2) *"*") + ((C - (Sr / 2)) *".")
             else:
                 board +="\n"
                 board += (((Sr / 3) *"*") + ((C - (Sr / 3)) *".") +"\n")
                 board += ((Sr / 3) *"*") + ((C - (Sr / 3)) *".")
         else :
             Sm = Sr + C
             board +="\n"
             board += (((Sm / 2) *"*") + ((C - (Sm / 2)) *".") +"\n")
             board += ((Sm / 2) *"*") + ((C - (Sm / 2)) *".")
                 
         list_board = list(board)
         list_board[len(list_board) - 1] = 'c'
         board = "".join(list_board)
     else:
         board +="\n"
         if(C == 1):
             board += M * "*\n"
             board += (R-M-1) * ".\n"
             board +=  "c"
         else:
             board += M * "*"
             board += (C-M-1) * "."
             board += "c"
             
     return board
        
        
        
 
 f_r = open('C.in',"r")
 n_test=int(f_r.readline().strip()) 
 f_w = open("C.out", "w")
 result = ""
 for i in range(n_test):
     R,C,M = map(int,f_r.readline().split())
     print R,C,M
     if(boardHasZero(R,C,M)):
         result = generateMineSweeperCase(R,C,M)
     else :
         result ="\nImpossible"
     print result
     output_str='Case #{itr}:{res}'.format(itr=(i+1),res=result)
     f_w.write(output_str+'\n')
     
 f_r.close()