import math
 
 def isPalindrome(s):
   length = len(s)
   for i in xrange(length / 2):
     if s[i] != s[length - 1 - i]: 
       return False
   return True
 
 n = int(raw_input())
 for i in range(n):
   a, b = map(int, raw_input().strip().split(' '))
   count = 0
   for j in range(a, b+1):
     if isPalindrome(str(j)):
       s = math.sqrt(j)
       if s == int(s) and isPalindrome(str(int(s))):
         count += 1
   print 'Case #%i: %i' % (i+1, count)
