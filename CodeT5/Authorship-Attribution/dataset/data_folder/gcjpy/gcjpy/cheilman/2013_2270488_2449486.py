#!/usr/bin/python
 
 import sys
 
 def readfile(file):
   """
     input:
 
 		T (number of test cases)
 
 		N M
 		N lines of M numbers (desired height of grass)
 
   """
 
   tests = []
 
   T = int(file.readline().strip())
 
   for i in xrange(T):
 		test = {}
 
 		line = file.readline().strip()
 		parts = line.split(' ')
 
 		if len(parts) != 2:
 			print "HORRIBLE ERROR in TEST %d!" % (i+1, )
 			return None
 
 		N = int(parts[0])
 		M = int(parts[1])
 
 		test['N'] = N
 		test['M'] = M
 		test['desired'] = []
     
 		for j in xrange(N):
 			line = file.readline().strip()
 			parts = line.split(' ')
 
 			if len(parts) != M:
 				print "TERRIBLE ERROR in TEST %d!" % (i+1, )
 				return None
 
 			for p in parts:
 				k = int(p)
 				test['desired'].append(k)
 
 		tests.append(test)
 
   return tests
 
 def run(test):
 	"""
 		Run a test and return output.
 	"""
 
 	# Figure out row/col min and max
 	test['row'] = []
 	test['col'] = []
 
 	for row in xrange(test['N']):
 		r = []
 
 		for col in xrange(test['M']):
 			i = row * test['M'] + col
 
 			r.append(test['desired'][i])
 
 		test['row'].append({'min' : min(r), 'max' : max(r)})
 
 	for col in xrange(test['M']):
 		c = []
 
 		for row in xrange(test['N']):
 			i = row * test['M'] + col
 
 			c.append(test['desired'][i])
 
 		test['col'].append({'min' : min(c), 'max' : max(c)})
 
 	for x in xrange(test['M']):
 		for y in xrange(test['N']):
 			i = y * test['M'] + x
 			v = test['desired'][i]
 
 			# If you are smaller than someone in both directions, it's impossible
 			rowmax = test['row'][y]['max']
 			colmax = test['col'][x]['max']
 			if (v < rowmax) and (v < colmax):
 				#print "(%d,%d) = %d, row = %d, col = %d" % (x, y, v, rowmax, colmax)
 				return "NO"
 
 	return "YES"
 
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
