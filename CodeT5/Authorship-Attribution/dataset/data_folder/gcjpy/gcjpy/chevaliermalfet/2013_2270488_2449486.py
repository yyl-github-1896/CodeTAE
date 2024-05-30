def isMowable(lawn):
     for i in range(len(lawn)):
         for j in range(len(lawn[i])):
             cellHeight = lawn[i][j]
             vertPossible = True
             horizPossible = True
             for k in range(len(lawn)):
                 if lawn[k][j] > cellHeight:
                     vertPossible = False
                     break
             for k in range(len(lawn[i])):
                 if lawn[i][k] > cellHeight:
                     horizPossible = False
                     break
             if not vertPossible and not horizPossible:
                 return "NO"
     return "YES"
 
 
 filename = "B-small-attempt0.in"
 outputname = filename + "out.txt"
 
 inFile = open(filename, 'r')
 outFile = open(outputname, 'w')
 
 
 numTests = int(inFile.readline())
 
     
 
 for i in range(numTests):
     dimensions = inFile.readline().split()
     n = int(dimensions[0])
     m = int(dimensions[1])
     lawn = []
     for j in range(n):
         line = inFile.readline().split()
         for k in range(m):
             line[k] = int(line[k])
         lawn += [line]
 
     answer = isMowable(lawn)
     
     
     outFile.write("Case #" + str(i+1) + ": " + answer + '\n')
     print "Case #" + str(i+1) + ": " + answer
 
 inFile.close()
 outFile.close()
