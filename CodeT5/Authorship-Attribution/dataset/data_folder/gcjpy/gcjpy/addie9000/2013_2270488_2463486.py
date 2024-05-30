#!/usr/local/bin/python
 import sys, string, math
 
 
 # check if num x is palindrome
 def is_palindrome(x):
     candidate = list(str(x))
     while len(candidate) > 1:
         if candidate.pop(0) != candidate.pop():
             return False
     return True
 
 
 #square
 def square(x):
     return x * x
 
 
 #solve case function
 def solve_case(ab, case_number):
     fs = 0
     root = int(math.sqrt(ab[0]))
     sq = square(root)
     if sq < ab[0]:
         root += 1
         sq = square(root)
 
     while sq <= ab[1]:
         if is_palindrome(root) and is_palindrome(sq):
             fs += 1
 
         #prepare for next
         root += 1
         sq = square(root)
 
     print "Case #%d: %d" % (case_number, fs)
 
 
 #main
 def main():
     r = sys.stdin
     if len(sys.argv) > 1:
         r = open(sys.argv[1], 'r')
 
     total_cases = r.readline()
     for case_number in range(1, int(total_cases) + 1):
         ab = map(int, r.readline().strip().split(' '))
         solve_case(ab, case_number)
 
 # invoke main
 if __name__ == "__main__":
     main()