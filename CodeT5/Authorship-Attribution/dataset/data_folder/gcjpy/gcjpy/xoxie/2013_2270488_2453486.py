import sys
 
 f = open( sys.argv[1] )
 t = f.readline()
 
 t = 1
 line = f.readline()
 while line != "":
     board = [line.strip(),
              f.readline().strip(),
              f.readline().strip(),
              f.readline().strip()]
 
     output = ""
 
     cols = [ "".join([x[y] for x in board]) for y in range(4)]
     diags = ["".join([x[y] for x,y in zip(board,range(4))]),
              "".join([x[y] for x,y in zip(board,range(-1,-5,-1))])]
     
     rows = board + cols + diags
 
     for row in rows:
         x = [1 for z in row if z is "X" or z is "T"]
         if sum(x) == 4:
             output = "X won"
             break
         o = [1 for z in row if z is "O" or z is "T"]
         if sum(o) == 4:
             output = "O won"
             break
     if output == "":
         finished = sum([ y.count(".") for y in board ])
         if finished == 0:
             output = "Draw"
         else:
             output = "Game has not completed"
     
     print "Case #%s: %s"%(t,output)
     t += 1
     line = f.readline()
     line = f.readline()
