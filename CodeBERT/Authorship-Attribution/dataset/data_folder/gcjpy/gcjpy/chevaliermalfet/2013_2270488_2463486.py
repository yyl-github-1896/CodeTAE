def isPalindrome(number):
     strNum = str(number)
     for i in range(len(strNum)/2 + 1):
         if strNum[i] != strNum[-1*(i+1)]:
             return False
     return True
 
 '''for i in range(40):
     if isPalindrome(i) and isPalindrome(i*i):
         print i*i
 '''
 
 
 filename = "C-small-attempt0.in"
 outputname = filename + "out.txt"
 
 inFile = open(filename, 'r')
 outFile = open(outputname, 'w')
 
 
 fairAndSquareNums = [1,4,9,121,484]
 
 numTests = int(inFile.readline())
 
 for i in range(numTests):
     line = inFile.readline().split()
     count = 0
     for j in range(int(line[0]), int(line[1])+1):
         if j in fairAndSquareNums:
             count += 1
     outFile.write("Case #" + str(i+1) + ": " + str(count) + '\n')
     print "Case #" + str(i+1) + ": " + str(count)
 
 inFile.close()
 outFile.close()
