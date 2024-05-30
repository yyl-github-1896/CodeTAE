import math
 
 def get_number_of_test_case():
     return int(raw_input().strip())
 
 def solve_case(t):
     A, B = [int(x) for x in raw_input().strip().split()]
 
     print 'Case #%d: %d' % (t, get_number_of_palindrome(B) - get_number_of_palindrome(A - 1),)
 
 def get_number_of_palindrome(n):
     ret = 0
 
     nt = int(math.floor(math.sqrt(n)))
     total_column = int(math.ceil(math.ceil(math.log10(nt + 1)) / 2.0))
     upper_limit = 10 ** total_column
 
     counter = 0
     while counter < upper_limit:
         c_str = [c for c in str(counter)]
         c_str.reverse()
 
         number = str(counter)
         for c in c_str:
             number += c
         number = int(number)
         number = number ** 2
         if number <= n and is_palindrome(number):
             ret += 1
 
         number = str(counter)
         for c in c_str[1:]:
             number += c
         number = int(number)
         number = number ** 2
         if number <= n and is_palindrome(number):
             ret += 1
         
         counter += 1
 
     return ret
 
 def is_palindrome(n):
     if n == 0:
         return False
     num = str(n)
     check_len = len(num) / 2
     ret = True
     for i in range(check_len):
         ret &= num[i] == num[-i - 1]
     return ret
 
 T = get_number_of_test_case()
 t = 1
 while t <= T:
     solve_case(t)
     t += 1
 
