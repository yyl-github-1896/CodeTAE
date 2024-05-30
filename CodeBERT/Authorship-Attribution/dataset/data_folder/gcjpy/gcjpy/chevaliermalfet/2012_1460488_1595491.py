inputFile = open("B-small-attempt0 (3).in", 'r')
 outputFile = open("dancingOutSmall.txt", 'w')
 numTests = int(inputFile.readline())
 
 def countDancers(n,s,p,totals):
     guaranteed = 0
     needSurprise = 0
     if p == 1:
         for total in totals:
             if total != 0:
                 guaranteed += 1
         return guaranteed
     for total in totals:
         if total >= p*3 - 2:
             guaranteed += 1
         elif total >= p*3 - 4:
             needSurprise += 1
     if needSurprise > s:
         return guaranteed + s
     else:
         return guaranteed + needSurprise
 
 for i in range(numTests):
     line = inputFile.readline().split()
     n = int(line[0])
     s = int(line[1])
     p = int(line[2])
     totals = []
     for j in range(n):
         totals += [int(line[3+j])]
     outputFile.write('Case #' + str(i+1) + ': ' + str(countDancers(n,s,p,totals)) + '\n')
 
 outputFile.close()
