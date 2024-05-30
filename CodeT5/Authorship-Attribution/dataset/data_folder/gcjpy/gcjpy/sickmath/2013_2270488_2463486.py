import math
 
 def isPalindrome(n) :
     return str(n) == str(n)[::-1]
 
 def findPalindrome(n) :
     if n % 2 == 0 : return [start*(10**(n/2)) + int(str(start)[::-1]) for start in range(10**(n/2-1),10**(n/2))]
     if n == 1 : return range(1,10)
     return [start*(10**(n/2)) + int(str(start)[:-1][::-1]) for start in range(10**(n/2),10**((n+1)/2))]
 
 def findPalindromeInRange(a, b) :
     num = range(len(str(a)), len(str(b)) + 1)
     allPalindrome = []
     for n in num : allPalindrome += findPalindrome(n)
     return filter(lambda x : a <= x <= b, allPalindrome)
 
 f = open('C-small-attempt0.in', 'r')
 g = open('output', 'w')
 
 T = int(f.readline()[:-1])
 
 for case in range(T) :
     A, B = map(int, f.readline()[:-1].split())
     a = int(math.ceil(A**0.5))
     b = int(B**0.5)
     res = len(filter(lambda x : isPalindrome(x**2), findPalindromeInRange(a, b)))
     outString = 'Case #' + str(case+1) + ': ' + str(res) + '\n'
     print outString[:-1]
     g.write(outString)
 
 f.close()
 g.close()
