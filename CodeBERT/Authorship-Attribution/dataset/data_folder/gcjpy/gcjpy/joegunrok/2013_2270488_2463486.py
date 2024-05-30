import sys
 
 lines = sys.stdin.readlines()
 def parseCase(lines):
     dims = map(int,lines[0].split(" "))
     return 1, dims
 
 def getCases(lines):
     i =0
     while i < len(lines):
         lines_used, case = parseCase(lines[i:])
         i += lines_used
         yield case
 
 import math
 
 fands = []
 phash = {1:True}
 def isPalindrome(p):
     return p in phash
 
 def test(p):
     square = p**.5
     return square == int(square) and isPalindrome(int(square))
 
 for i in range(1,10**5):
     if i > 9:
         small_p = int(i * 10 ** int(math.log(i,10)) + int("".join(reversed(str(i)[:-1]))))
     else: small_p = i
     phash[small_p]= test(small_p)
     if phash[small_p]: fands.append(small_p)
     big_p = int(i * 10 ** int(math.log(i,10)+1) + int("".join(reversed(str(i)))))
     phash[big_p] = test(big_p)
     if phash[big_p]: fands.append(big_p)
 cNum =0
 
 for c in getCases(lines[1:]):
     cNum += 1
     answer = []
     for i in fands:
         if i < c[0]: continue
         if i > c[1]: break
         if phash[i]: answer.append(i)
     answer = str(len(answer))
     print "Case #%d: %s" % ( cNum, answer)
 
 
     
 
 
