import sys
 #sys.stdin = open("c_example.in")
 
 n_cases = input()
 
 def to_ints(s):
     return map(int, s.split())
 
 def is_palindrome(n):
     s = str(n)
     return s == s[::-1]
 
 for case in xrange(1, n_cases + 1):
     a, b = to_ints(raw_input())
 
     nums = range(int(b ** .5) + 2)
     palins = filter(is_palindrome, nums)
     squares = [x**2 for x in palins]
     palin_squares = filter(is_palindrome, squares)
     range_squares = [x for x in palin_squares if a <= x <= b]
 
     print "Case #%d: %s" % (case, len(range_squares))
