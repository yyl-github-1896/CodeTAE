fileName = raw_input("File name: ")
 f = open(fileName,"r")
 
 
 n = int(f.readline()[:-1])
 
 def check_row(board, index):
     row = board[index]
     M = row[0]
     index = 0
     for i in range(len(row)):
         num = row[i]
         if(num > M):
             M = num
             index = i
     for i in range(len(row)):
         num = row[i]
         if(num < M):
             if not check_col(board,i,num):
                 return False
     return True
 
 
 def check_col(board,index,number):
     for i in range(len(board)):
         if board[i][index] > number:
             return False
     return True
 
 def check_all(board):
     for i in range(len(board)):
         if not check_row(board, i):
             return False
     return True    
  
 outputFileName = raw_input("output file name: ")
 of = open(outputFileName,"w")
 
 for i in range(n):
     board = []
     mn = f.readline()[:-1].split()
     m = int(mn[0])
     n = int(mn[1])
     for j in range(m): 
         row = f.readline()[:-1].split()
         #print row
         row_lst = []
         for s in row:
             row_lst += [int(s)]
         board += [row]
     if check_all(board):
         of.write( "Case #%d: %s\n" %(i+1, "YES"))
     else:
         of.write( "Case #%d: %s\n" %(i+1, "NO"))
 
 of.close()
 f.close()
 
 #print might_have_finished, boards
 
 ##for i in range(n): # print out
 ##    print "Case #%d: %s" %(i+1, translate(cases[i]))
     
     
 
 
     
