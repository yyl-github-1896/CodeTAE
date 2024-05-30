__author__ = 'Jeffrey'
 
 # inFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\C-sample.in"
 inFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\C-small-attempt0.in"
 # inFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\C-large.in"
 
 outFileName = inFileName[: -2] + "out"
 
 
 def parseInput(f):
     T = int(f.readline())
     L = []
 
     for i in range(T):
         L.append([int(i) for i in f.readline().split()])
 
     return T, L
 
 
 def calculateOneClick(R, C, M):
     size = R * C
     if R == 1 or C == 1 and M < size:
         return generateWinBoardBaseCase(R, C, M)
     elif size - M == 1:
         return generateWinBoardBaseCase(R, C, M)
     elif size - M >= 4:
         return generateWinBoard(R, C, M)
     return "Impossible"
 
 def generateWinBoard(R,C,M):
     emptySpace = R * C - M - 4
     out = "c"
     if C > 1:
         out += "."
         for i in range(2,C):
             if emptySpace > 0:
                 out += "."
                 emptySpace -= 1
             else:
                 out += "*"
                 # out += '\n'
     if R > 1:
         out += '\n'
         out += "."
         if C > 1:
             out += "."
         for i in range(2,C):
             if emptySpace > 0:
                 out += "."
                 emptySpace -= 1
             else:
                 out += "*"
     for r in range(2,R):
         out += '\n'
         for c in range(C):
             if emptySpace > 0:
                 out += "."
                 emptySpace -= 1
             else:
                 out += "*"
     return out
 
 def generateWinBoardBaseCase(R,C,M):
     emptySpace = R * C - M - 1
     out = "c"
     if C > 1:
         for c in range(1,C):
             if emptySpace > 0:
                 out += "."
                 emptySpace -= 1
             else:
                 out += "*"
     for r in range(1,R):
         out += '\n'
         for c in range(C):
             if emptySpace > 0:
                 out += "."
                 emptySpace -= 1
             else:
                 out += "*"
     return out
 
 
 def playGame(T, L):
     for i in range(T):
         result = calculateOneClick(L[i][0], L[i][1], L[i][2])
         yield "Case #" + str(i + 1) + ":\n" + str(result)
 
 
 if __name__ == "__main__":
     iF = open(inFileName, 'r')
     T, L = parseInput(iF)
     iF.close()
 
     print(T)
     print(L)
 
     oF = open(outFileName, "wb")
     for out in playGame(T, L):
         print(out)
         # print(bytes(out, 'utf-8'), file=oF)
         oF.write(bytes(out + "\n", 'utf-8'))
     oF.close()
