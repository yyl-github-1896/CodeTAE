def is_palindrome(s):
 	if s == '':
 		return True
 	else:
 		if (ord(s[0]) - ord(s[len(s)-1])) == 0:
 			return is_palindrome(s[1 : len(s) - 1])
 		else:
 			return False
 
 all_fair_and_square = set()
 for i in range(10000):
 	orig = str(i)
 	rev = orig[::-1]
 
 	palin = orig + rev
 	intpalin = int(palin)
 	if is_palindrome(str(intpalin * intpalin)):
 		all_fair_and_square.add(intpalin * intpalin)
 
 	palin = orig[:-1] + rev
 	intpalin = int(palin)
 	if is_palindrome(str(intpalin * intpalin)):
 		all_fair_and_square.add(intpalin * intpalin)
 	
 
 import sys
 
 t = int(sys.stdin.readline().strip())
 for ii in range(t):
 	line = sys.stdin.readline().strip().split()
 	a = int(line[0])
 	b = int(line[1])
 	count = 0
 	for num in all_fair_and_square:
 		if (num >= a) and (num <= b):
 			count += 1
 	print "Case #" + str(ii + 1) + ": " + str(count)
 
