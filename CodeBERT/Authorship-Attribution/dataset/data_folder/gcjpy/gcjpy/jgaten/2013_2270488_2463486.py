#!/usr/bin/env python
 import sys
 
 from itertools import count
 
 def palindromes():
     # it's not straightforward to get the numbers in order...
     for digits in count(1):
         for n in xrange(10**(digits-1), 10**digits):
             n = str(n)
             yield int(n + n[-2::-1])
         for n in xrange(10**(digits-1), 10**digits):
             n = str(n)
             yield int(n + n[::-1])
 
 def is_palindrome(n):
     n = str(n)
     return n == n[::-1]
 
 def solve(A, B):
     # Loop through palindromic numbers and check that their squares are palindromes.
     count = 0
     for n in palindromes():
         square = n**2
         if square > B:
             break
         if square >= A and is_palindrome(square):
             count += 1
     return count
 
 if __name__ == '__main__':
     with open(sys.argv[1], 'rU') as fin, open(sys.argv[2], 'w') as fout:
         T = int(fin.readline())
         for case in xrange(1, T+1):
 
             A, B = map(int,fin.readline().split())
             soln = solve(A, B)
 
             print >> fout, "Case #{0}: {1}".format(case, soln)
