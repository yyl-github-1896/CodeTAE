import sys
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())
     for _t in range(t):
         X = int(f.readline())
         cardsX = [[int(y) for y in f.readline().split()] for x in range(4)]
         row = cardsX[X-1]
         Y = int(f.readline())
         cardsY = [[int(y) for y in f.readline().split()] for x in range(4)]
         column = cardsY[Y-1]
         card = [x for x in row if x in column]
         if len(card) > 1:
             answer = "Bad magician!"
         elif len(card) == 0:
             answer = "Volunteer cheated!"
         else:
             answer = str(card[0])
         print ("Case #" + str(_t+1) + ": " + answer)
     
 
