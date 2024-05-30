'''
 Created on 2012-4-14
 
 @author: hemnd
 '''
 def cal(A, B):
     rslt = 0
     tmp = []
     for i in range(1, len(A)):
         min = max = 0
         for j in range(int(A[0:i]), int(B[0:i]) + 1):
             sJ = str(j)
             sMin = (sJ * (len(A) - i))[0:len(A) - i]
             min = int(sMin)
             if int(sMin + sJ) <= int(sJ + sMin):
                 min += 1
             if int(B[-i:]) >= j:
                 max = int(B[:(len(A) - i)])
             else:
                 max = int(B[:(len(A) - i)]) - 1
             if max < min:
                 continue
             for k in range(min, max + 1):
                 if (sJ + str(k), str(k) + sJ) in tmp:
                     print (sJ + str(k), str(k) + sJ), 'already there'
                     continue
                 else:
                     tmp.append((sJ + str(k), str(k) + sJ))
                     rslt += 1
 
 #            rslt = rslt + max - min + 1
     return rslt
 
 inputFile = open('C-small-attempt2.in', 'r')
 #inputFile = open('test.txt', 'r')
 inputLines = inputFile.readlines()
 inputFile.close()
 
 T = int(inputLines[0])
 outputLines = []
 
 for i in range(1, T + 1):
     args = inputLines[i].strip().split(' ')
     outputLines.append('Case #%d: %d\n' % (i, cal(args[0], args[1])))
     print outputLines[i - 1],
 
 outputFile = open('C-small.out', 'w')
 outputFile.writelines(outputLines)
 outputFile.close()
