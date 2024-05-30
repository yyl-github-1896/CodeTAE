#!/usr/bin/python
 
 def readfile(filename):
 	"""
 	The first line of the input gives the number of test cases,
 	T. T test cases follow. Each test case consists of a single line
 	containing the integers A and B.
 	"""
 
 	file = open(filename, "rt")
 
 	retval = {}
 
 	T = int(file.readline().strip())
 	retval['T'] = T
 
 	tests = []
 
 	for i in xrange(T):
 		line = file.readline().strip()
 
 		parts = line.split(" ")
 
 		A = int(parts[0])
 		B = int(parts[1])
 
 		test = {'A' : A, 'B' : B}
 
 		tests = tests + [test, ]
 
 	retval['tests'] = tests
 
 	return retval
 
 def isrecycled(n, m):
 	if (len(n) != len(m)):
 		return False
 
 	for i in range(len(n)):
 		left = n[:i]
 		right = n[i:]
 
 		flip = right + left
 
 		if (flip == m):
 			return True
 
 	return False
 
 def process(test):
 	count = 0
 
 	A = test['A']
 	B = test['B']
 
 	for n in xrange(A, B):
 		for m in xrange(n + 1, B):
 			if (isrecycled(str(n), str(m))):
 				count = count + 1
 
 	return count
 
 def process2(test):
 	count = 0
 
 	A = test['A']
 	B = test['B']
 
 	for n in xrange(A, B):
 		v = str(n)
 
 		found = set()
 
 		for i in xrange(len(v)):
 			left = v[:i]
 			right = v[i:]
 
 			flip = right + left
 			iflip = int(flip)
 
 			if ((iflip > n) and (iflip <= B)):
 				if (not iflip in found):
 					count = count + 1
 					found.add(iflip)
 
 	return count
 
 data = readfile("C-small-attempt0.in")
 
 for i in xrange(data['T']):
 	test = data['tests'][i]
 
 	result = process2(test)
 
 	print "Case #%d: %d" % (i + 1, result)
