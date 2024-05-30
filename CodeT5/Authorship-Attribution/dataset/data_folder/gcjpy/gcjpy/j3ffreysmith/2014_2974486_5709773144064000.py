__author__ = 'Jeffrey'
 
 inFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\B-small-attempt0.in"
 outFileName = inFileName[ : -2] + "out"
 
 
 def parseInput(f):
     T = int(f.readline())
     L = []
 
     for i in range(T):
         L.append([float(i) for i in f.readline().split()])
 
     return T, L
 
 
 def calculateWinTime(C, F, X):
     R = 2.0 # rate of cookie profit (cookies/s)
     totalTime = 0.0
     while (X / R >= C/R + X/(R + F)):
         totalTime += C / R
         R += F
     return totalTime + X / R
 
 
 def playGame(T,L):
     for i in range(T):
         result = calculateWinTime(L[i][0], L[i][1], L[i][2])
         yield "Case #" + str(i + 1) + ": " + "{:0.7f}".format(result)
 
 
 if __name__=="__main__":
     iF = open(inFileName, 'r')
     T, L = parseInput(iF)
     iF.close()
 
     print(T)
     print(L)
 
     oF = open(outFileName, "wb")
     for out in playGame(T, L):
         print(out)
         # print(bytes(out, 'utf-8'), file=oF)
         oF.write(bytes(out + "\n",'utf-8'))
     oF.close()
