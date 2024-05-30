inputFile = open("C-small-attempt0.in", 'r')
 outputFile = open("recycleOut.txt", 'w')
 numTests = int(inputFile.readline())
 
 def countRecycle(a,b):
     count = 0
     for n in range(a,b):
         for m in range(n+1,b+1):
             nStr = str(n)
             canRecycle = False
             for k in range(len(nStr)):
                 if nStr[k:] + nStr[0:k] == str(m):
                     canRecycle = True
                     break
             if canRecycle:
                 count += 1
     return count
 
 for i in range(numTests):
     line = inputFile.readline().split()
     a = int(line[0])
     b = int(line[1])
     outputFile.write('Case #' + str(i+1) + ': ' + str(countRecycle(a,b)) + '\n')
 
 inputFile.close()
 outputFile.close()
