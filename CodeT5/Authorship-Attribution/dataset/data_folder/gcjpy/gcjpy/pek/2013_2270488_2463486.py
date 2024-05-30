import sys
 import bisect
 
 def is_palindrome(n):
     s = str(n)
     return s == s[::-1] 
 
 palindromes = [[], [1,2,3,4,5,6,7,8,9], [11,22,33,44,55,66,77,88,99]]
 all_palindromes = palindromes[1] + palindromes[2]
 limit = [100]
 
 palindromic_squares = []
 psqtop = 0
 psqix = 0
 
 stdin = sys.stdin
 for c in xrange(int(stdin.readline())):
     a,b = map(int, stdin.readline().split())
 
     while psqtop < b:
         while psqix >= len(all_palindromes):
             ps = []
             pp = 10 ** (len(palindromes)-1) + 1
             for i in range(1,10):
                 for p in palindromes[-2]:
                     ps.append(i * pp + 10 * p) 
             palindromes.append(ps)
             all_palindromes.extend(ps)
 
         sq = all_palindromes[psqix] * all_palindromes[psqix]
         if is_palindrome(sq):
             palindromic_squares.append(sq)
         psqix  += 1
         psqtop = sq
 
     aix = bisect.bisect_left(palindromic_squares, a)
     bix = bisect.bisect_right(palindromic_squares, b)
 
     print "Case #%i: %i" % (c+1, bix-aix) 
