'''
 Created on Apr 12, 2013
 
 @author: Moatasem
 '''
 
 def getStatus(board):
     status="" 
     solved=False
     n_dotted=0
     #checking for columns and rows
     for i in range(4):
         result= checkBoard(board[i])
         if(result!="None"):
             status=result
             solved=True
         else:
             columnlist=[]
             for j in range(4):
                 if(board[i][j]=='.'):
                     n_dotted+=1
                 columnlist.append(board[j][i])
             result= checkBoard(columnlist)
             if(result!="None"): 
                 solved=True
                 status=result
                 break
         if(solved):
             break
         
     #checking for diagonals
     result_l=checkBoard([board[x][x] for x in range(4)]) #leftDiagonal
     result_r=checkBoard([board[0][3],board[1][2],board[2][1],board[3][0]]) #rightDiagonal
     if(result_l!="None"): 
             solved=True
             status=result_l
     if(result_r!="None"): 
             solved=True
             status=result_r
                 
     if(solved==False):
         if(n_dotted==0):
             status="Draw"
         else: 
             status="Game has not completed"   
 
     return status
 
 
 def checkBoard(board):
         status="None"
         x_count=board.count('X')
         o_count=board.count('O')
         t_count=board.count('T')
         if(x_count==4 or (x_count==3 and t_count==1)):
             status="X won"
         elif(o_count==4 or (o_count==3 and t_count==1)):
             status="O won"
         return status
 
 
 f_r = open('A.in',"r")
 n_test=int(f_r.readline().strip()) 
 
 f_w = open("A.out", "w")
 for i in range(n_test):
     board=[]
     for j in range(4):
         board.append(f_r.readline().strip())
     result= getStatus(board)
     output_str='Case #{itr}: {res}'.format(itr=(i+1),res=result)
     f_w.write(output_str+'\n')
     f_r.readline()
 f_r.close()
 f_w.close()
