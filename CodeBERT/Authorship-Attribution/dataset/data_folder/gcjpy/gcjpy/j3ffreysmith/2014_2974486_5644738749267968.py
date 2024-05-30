__author__ = 'Jeffrey'
 
 # inFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\D-sample.in"
 inFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\D-small-attempt0.in"
 # inFileName = "C:\\Users\\Jeffrey\\IdeaProjects\\Google Code Jam 2014\\D-large.in"
 
 outFileName = inFileName[: -2] + "out"
 
 
 def parseInput(f):
     T = int(f.readline())
     L = []
 
     for i in range(T):
         f.readline()
         L.append(([float(j) for j in f.readline().split()], [float(j) for j in f.readline().split()]))
         L[-1][0].sort()
         L[-1][1].sort()
 
     return T, L
 
 
 def calculateScores(naomi, ken):
     return [calcDeceit(naomi, ken), calcHonest(naomi, ken)]
 
 def calcDeceit(naomi, ken):
     wins = 0
     while len(naomi) > 0:
         if naomi[-1] > ken[-1]:
             naomi = naomi[ : -1]
             ken = ken[ : -1]
             wins += 1
         else:
             naomi = naomi[1: ]
             ken = ken[ : -1]
     return wins
 
 def calcHonest(naomi, ken):
     wins = 0
     while len(naomi) > 0:
         n = naomi.pop(0)
         k = ken[0]
         for i in range(len(ken)):
             kTemp = ken[i]
             if kTemp > n:
                 k = ken.pop(i)
                 break
         else:
             ken.pop(0)
             wins += 1
     return wins
 
 
 
 def playGame(T, L):
     for i in range(T):
         result = calculateScores(L[i][0], L[i][1])
         yield "Case #{}: {} {}".format(i + 1, result[0], result[1])
 
 
 if __name__ == "__main__":
     iF = open(inFileName, 'r')
     T, L = parseInput(iF)
     iF.close()
 
     print(T)
     for l in L:
         print()
         for k in l:
             print(k)
 
     oF = open(outFileName, "wb")
     for out in playGame(T, L):
         print(out)
         # print(bytes(out, 'utf-8'), file=oF)
         oF.write(bytes(out + "\n", 'utf-8'))
     oF.close()
