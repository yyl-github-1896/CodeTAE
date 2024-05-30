__author__ = 'Jeffrey'
 
 inFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\A-small-attempt0.in"
 outFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\A-small-attempt0.out"
 
 
 def parseInput(f):
     T = int(f.readline())
     L = []
 
     for i in range(T):
         picks = []
         cards = []
         for j in range(2):
             picks.append( int(f.readline()))
             tempL = []
             for k in range(4):
                 tempL.append( [int(j) for j in f.readline().split()])
             cards.append(tempL)
         L.append((picks, cards))
 
     return T, L
 
 
 def performTrick(picks, cards):
     matchFound = False
     matchedCard = None
     for card in cards[0][picks[0] - 1]:
         possibleMatch = card in cards[1][picks[1] - 1]
         if possibleMatch and matchFound:
             return "Bad magician!"
         elif possibleMatch:
             matchFound = True
             matchedCard = card
     if matchFound:
         return matchedCard
     else:
         return "Volunteer cheated!"
 
 
 def playGame(T,L):
     for i in range(T):
         result = performTrick(L[i][0], L[i][1])
         yield "Case #" + str(i + 1) + ": " + str(result)
 
 
 if __name__=="__main__":
     iF = open(inFileName, 'r')
     T, L = parseInput(iF)
     iF.close()
 
     oF = open(outFileName, "wb")
     for out in playGame(T, L):
         # print(out)
         # print(bytes(out, 'utf-8'), file=oF)
         oF.write(bytes(out + "\n",'utf-8'))
     oF.close()
