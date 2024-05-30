#!/usr/bin/python3
 #
 # Some notes:
 # - It's better to find palindromes in the square rooted numbers (there will be a lot fewer)
 # - It's also much faster to generate the palindromes than to detect if a random number is a palindrome
 #   - Number of palindromes with n digits: 10^(ceil(n/2))
 #   - E.g, 3 digits => 10^2  -  4 digits => 10^2  -  5 digits => 10^3
 # - So the problem is reduced to generate the palindromes which are still palindromes when squared
 #
 # - And how to detect is a squared palindrome is still a palindrome? Easy, let's draw a multiplication:
 #          1 2 1
 #          1 2 1
 #       --------
 #          1 2 1
 #        2 4 2
 #      1 2 1
 #      ---------
 #      1 4 6 4 1
 #
 #   - The extreme case is the central column. If the sum is >=10, then resulting number will not be a palindrome
 #   - As the original number is a palindrome, this central column will always be the sum of the squares of all
 #     the digits in the number. E.g: 121 => 1^2 + 2^2 + 1^2 = 1 + 4 + 1 = 6 => less than 10 => square is a palindrome
 #   - This means that palindromes with digits 4-9 can never become a palindrome when squared
 #   - 3 can only appear once => 3 is the only valid number containing digit 3
 #   - 2 can appear at most twice:
 #     - 2 twos + 0/1 one (in this case 2 have to be the first and last digit)
 #     - 1 two + 0/2/4 ones (in this case 2 has to be in the middle position)
 #   - 1 can appear alone up to 9 times
 #   - 0 can appear as many times as you want
 #
 
 
 import sys
 import math
 
 # This is the same as findpalindromes, but much faster (it just calculates the combinations
 # instead of obtaining all the actual numbers)
 def calculatepalindromes(ndigits):
     # Special case: only 1 digit
     if ndigits == 1:
         return 3
 
     result = 0
     isEven = ndigits % 2 == 0
     fillingdigits = math.floor((ndigits - 2)/2)
 
     # Palindromes with 2's
     if isEven:
         result += 1
     else:
         result += 3
 
     # Palindromes with only 1's
     for numones in range(0, min(6, fillingdigits) + 1):
         combinations = int(math.factorial(fillingdigits) / (math.factorial(fillingdigits-numones) * math.factorial(numones)))
         result += combinations
         if not isEven:
             result += combinations
 
     return result
 
 
 def findpalindromes(ndigits):
     # Special case: only 1 digit
     if ndigits == 1:
         return [1, 2, 3]
 
     result = []
     isEven = ndigits % 2 == 0
     fillingdigits = math.floor((ndigits - 2)/2)
 
     # Palindromes with 2's
     if isEven:
         result.append(int("2" + "0"*(fillingdigits*2) + "2"))
     else:
         result.append(int("2" + "0"*fillingdigits + "0" + "0"*fillingdigits + "2"))
         result.append(int("2" + "0"*fillingdigits + "1" + "0"*fillingdigits + "2"))
         result.append(int("1" + "0"*fillingdigits + "2" + "0"*fillingdigits + "1"))
 
     # Palindromes with only 1's
     for numones in range(0, min(6, fillingdigits)+1):
         ones = fillOnes([], fillingdigits, numones)
         for o in ones:
             if isEven:
                 result.append(int("1" + "".join(o) + "".join(list(reversed(o))) + "1"))
             else:
                 result.append(int("1" + "".join(o) + "0" + "".join(list(reversed(o))) + "1"))
                 result.append(int("1" + "".join(o) + "1" + "".join(list(reversed(o))) + "1"))
 
     return result
 
 def fillOnes(combination, size, remainingOnes):
     if len(combination) == size:
         return [combination]
     result = []
     if remainingOnes > 0:
         c = combination + ["1"]
         result += fillOnes(c, size, remainingOnes - 1)
     if remainingOnes < size - len(combination):
         c = combination + ["0"]
         result += fillOnes(c, size, remainingOnes)
     return result
 
 
 
 ncases = int(sys.stdin.readline())
 
 for t in range(1, ncases+1):
     fairsquare = 0
     (a, b) = sys.stdin.readline().strip().split(" ")
     intA = int(a)
     intB = int(b)
     ndigitsA = len(a)
     ndigitsB = len(b)
     ndigitsARooted = math.ceil(ndigitsA/2)
     ndigitsBRooted = math.ceil(ndigitsB/2)
 
     if ndigitsBRooted == ndigitsARooted:
         palindromes = findpalindromes(ndigitsARooted)
         for p in palindromes:
             if p ** 2 >= intA and p ** 2 <= intB:
                 fairsquare +=1
     else:
         palindromes = findpalindromes(ndigitsARooted)
         for p in palindromes:
             if p ** 2 >= intA:
                 fairsquare +=1
 
         for i in range(ndigitsARooted + 1, ndigitsBRooted):
             fairsquare += calculatepalindromes(i)
 
         palindromes = findpalindromes(ndigitsBRooted)
         for p in palindromes:
             if p ** 2 <= intB:
                 fairsquare +=1
 
     print("Case #%d: %d" % (t, fairsquare))
