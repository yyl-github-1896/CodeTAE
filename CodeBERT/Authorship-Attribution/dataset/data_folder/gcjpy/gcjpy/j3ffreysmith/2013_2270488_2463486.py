import math
 
 #wont help, runs out of memory for 10^100
 # palindromeCache = {} #ideally this is precalculated
 
 # def isPalindrome(S):
 	# s = str(S) #so I dont need to make sure its a string
 	# if s in palindromeCache:
 		# return palindromeCache[s]
 		
 	# palindromeCache[s] = True
 	# for i in range(len(s)//2):
 		# if not s[i] == s[-1 - i]:
 			# palindromeCache[s] = False
 			# break
 	# return palindromeCache[s]
 	
 def isPalindrome(S):
 	s = str(S) #so I dont need to make sure its a string
 	for i in range(len(s)//2):
 		if not s[i] == s[-1 - i]:
 			return False
 	return True
 
 def FairAndSquare(infile="C-small-attempt0.in", outfile="C-small-attempt0.out"):
 	inF = open(infile, 'r')
 	outF = open(outfile, 'w')
 	
 	for t in range(1, int(inF.readline().strip()) + 1):
 		temp = inF.readline().strip().split()
 		A = long(temp[0])
 		B = long(temp[1])
 		count = long(0)
 		
 		i = long(math.ceil(math.sqrt(A)))
 		m = long(math.floor(math.sqrt(B)))
 		while i <= m:
 			if isPalindrome(i):
 				if isPalindrome(i**2):
 					count += 1
 			i += 1
 					
 		outF.write("Case #" + str(t) + ": " + str(count) + "\n")
 	
 	#closing files
 	inF.close()
 	outF.close()
 	
 	#so I dont need to cat the file after
 	f = open(outfile, 'r')
 	print f.read()
 	f.close()
 	
 	
 if __name__ == "__main__":
     FairAndSquare()