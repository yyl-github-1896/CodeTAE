import sys
 
 def decode_data(input):
     output = ""
     Total = 0
     for row in input:
         T = row.count("T")
         X = row.count("X")
         O = row.count("O")
         #print (row, T, X, O, Total)
         if X + T == 4:
             return "X won"
         elif O + T == 4:
             return "O won"
         else:
             Total += T + X + O
             
     rotated = zip(*input[::-1])
     for row in rotated:
         T = row.count("T")
         X = row.count("X")
         O = row.count("O")
         if X + T == 4:
             return "X won"
         elif O + T == 4:
             return "O won"
 
     row = [input[x][x] for x in range(4)]
     row.count("T")
     X = row.count("X")
     O = row.count("O")
     if X + T == 4:
         return "X won"
     elif O + T == 4:
         return "O won"
 
     row = [input[3-x][x] for x in range(4)]
     T = row.count("T")
     X = row.count("X")
     O = row.count("O")
     if X + T == 4:
         return "X won"
     elif O + T == 4:
         return "O won"
 
     if Total < 16:
         return "Game has not completed"
     else:
         return "Draw"
     return output
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())
     for _t in range(t):
         s = [f.readline() for i in range(4)]
         print ("Case #" + str(_t+1) + ": " + decode_data(s))
         f.readline()
     
 
