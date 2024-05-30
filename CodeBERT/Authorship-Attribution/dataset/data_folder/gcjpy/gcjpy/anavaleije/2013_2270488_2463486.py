import sys, math
 
 def isPalindrome(n):
 	n = str(n)	
 	for i in xrange(len(n)/2):
 		if n[i] != n[(-i-1)]:
 			return False
 	return True
 
 ##########################################################
 # Main
 
 inputFileName = sys.argv[1]
 
 f = file(inputFileName)
 fout = file("output.txt", "w")
 
 T = eval(f.readline())
 
 for case in xrange(T):
 	data = f.readline().split()
 	A = eval(data[0])
 	B = eval(data[1])
 
 	i = A
 	found = []
 	while i <= B:
 		if isPalindrome(i):
 			sqrtI = math.sqrt(i)
 			if sqrtI == int(sqrtI):
 				if isPalindrome(int(sqrtI)):
 					found.append(i)
 		i += 1
 
 	##### Output writing
 	fout.write("Case #%d: %d\n" %(case + 1, len(found)))
