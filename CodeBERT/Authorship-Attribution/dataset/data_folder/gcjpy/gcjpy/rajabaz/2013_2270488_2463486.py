from math import sqrt
 
 def isqrt(num):
     return int(sqrt(num))
 
 def is_square(num):
     return isqrt(num)**2 == num
 
 def is_palindrome(num):
     return str(num) == "".join(reversed(str(num)))
 
 def is_fair_and_square(num):
     return is_square(num) and is_palindrome(num) and is_palindrome(isqrt(num))
 
 def solve(A,B):
     count = 0
     for i in range(A,B+1):
         if is_fair_and_square(i):
             count += 1
     return count
 
 if __name__ == "__main__":
     T = int(raw_input())
     for i in range(1, T+1):
         A,B = [int(x) for x in raw_input().split()]
         print "Case #%d: %d" % (i, solve(A,B))
         
