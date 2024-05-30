# -*- coding: utf-8 -*-
 
 N_MAX = 10 ** 7  # for First large dataset
 
 
 def is_palindrome(n):
     s = str(n)
     for i in xrange(len(s) / 2):
         if s[i] != s[-1 - i]:
             return False
     return True
 
 palindromes = [x for x in xrange(N_MAX) if is_palindrome(x)]
 palindrome_squares = [x ** 2 for x in palindromes]
 fair_and_square_palindromes = filter(is_palindrome, palindrome_squares)
 
 
 T = int(raw_input())
 for test_case_id in xrange(1, T + 1):
     A, B = map(int, raw_input().split())
     answer = len([x for x in fair_and_square_palindromes if A <= x <= B])
     print 'Case #{}: {}'.format(test_case_id, answer)
