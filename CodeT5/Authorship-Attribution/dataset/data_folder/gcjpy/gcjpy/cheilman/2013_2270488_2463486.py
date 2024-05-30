#!/usr/bin/python
 
 import sys
 import math
 
 def readfile(file):
   """
     input:
 
 		T (number of test cases)
 
 		A B
 
   """
 
   tests = []
 
   T = int(file.readline().strip())
 
   for i in xrange(T):
 		test = {}
 
 		line = file.readline().strip()
 		parts = line.split(" ")
 
 		if len(parts) != 2:
 			print "HORRIBLE ERROR IN TEST CASE %d" % (i+1,)
 			return None
 
 		test['A'] = int(parts[0])
 		test['B'] = int(parts[1])
     
 		tests.append(test)
 
   return tests
 
 def isPalindrome(s):
 	"""
 		Is s a palindrome.
 
 		S must be a string.
 	"""
 
 	l = len(s)
 
 	if (l % 2) == 0:
 		# even
 		frontHalf = s[0:l/2]
 		backHalf = s[l/2:]
 	else:
 		# odd
 		frontHalf = s[0:(l-1)/2]
 		backHalf = s[(l+1)/2:]
 
 	backHalf = backHalf[::-1]
 
 	if frontHalf == backHalf:
 		return True
 	else:
 		return False
 
 def isFairAndSquare(n):
 
 	sqrtN = int(math.sqrt(n))
 
 	if (sqrtN * sqrtN) != n:
 		#print "%d is not square" % (n, )
 		return False
 
 	if not isPalindrome(str(n)):
 		#print "%d is not palindrome" % (n, )
 		return False
 
 	if not isPalindrome(str(sqrtN)):
 		#print "sqrt(%d) = %d is not palindrome" % (n, sqrtN)
 		return False
 
 	return True
 
 def run(test):
 	"""
 		Run a test and return output.
 	"""
 
 	count = 0
 
 	for i in xrange(test['A'], test['B'] + 1):
 		if isFairAndSquare(i):
 			count = count + 1
 
 	return count
 
 	i = int(math.sqrt(test['A']))
 
 	if (i * i) < test['A']:
 		i = i + 1
 
 	# Generate squares from palindromes
 	while i < test['B']:
 		#print "Checking %d" % (i, )
 		if not isPalindrome(str(i)):
 			i = i + 1
 			continue
 
 		# square it
 		s = i * i
 
 		if s <= test['B']:
 			if isPalindrome(str(s)):
 				#print "Counting %d" % (i * i, )
 				count = count + 1
 		else:
 			# all done
 			break
 
 		i = i + 1
 
 	return "%s" % (count, )
 
 file = open(sys.argv[1], "rt")
 
 tests = readfile(file)
 
 file.close()
 
 case = 1
 
 for test in tests:
 #if True:
   #test = tests[0]
   result = run(test)
   print "Case #%d: %s" % (case, result)
   case = case + 1
