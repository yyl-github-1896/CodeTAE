#!/usr/bin/python
 
 def readfile(filename):
 	"""
 		The first line of the input gives the number of test
 		cases, T. T test cases follow. Each test case consists of
 		a single line containing integers separated by single
 		spaces. The first integer will be N, the number of
 		Googlers, and the second integer will be S, the number
 		of surprising triplets of scores. The third integer will
 		be p, as described above. Next will be N integers ti:
 		the total points of the Googlers.
 	"""
 
 	file = open(filename, "rt")
 
 	retval = {}
 
 	T = int(file.readline().strip())
 	retval['T'] = T
 
 	tests = []
 
 	for i in xrange(T):
 		line = file.readline().strip()
 
 		parts = line.split(" ")
 
 		N = int(parts[0])
 		S = int(parts[1])
 		p = int(parts[2])
 		t = []
 
 		for j in xrange(N):
 			t = t + [int(parts[3 + j]), ]
 
 		test = { 'N' : N, 'S': S, 'p' : p, 't' : t }
 		tests = tests + [test, ]
 
 	retval['tests'] = tests
 	return retval
 
 def spread(triplet):
 	return max(abs(triplet[0] - triplet[1]), abs(triplet[1] - triplet[2]), abs(triplet[2] - triplet[0]))
 
 def bestresult(triplet):
 	if triplet:
 		return max(triplet)
 	return 0
 
 def getcombos(points):
 	"""
 		Returns ([unsurprising possibilities, ], [surprising possibilities])
 	"""
 
 	unsurps = []
 	surps = []
 
 	avg = points / 3.0
 
 	# Go from (avg-2) to (avg+3) to account for rounding
 	avg = int(avg)
 
 	tested = []
 
 	for i in xrange(max(avg - 2, 0), min(avg + 3, 10)+1):
 		for j in xrange(max(avg - 2, 0), min(avg + 3, 10)+1):
 			for k in xrange(max(avg - 2, 0), min(avg + 3, 10)+1):
 				if (i + j + k) != points:
 					continue
 
 				scores = (i,j,k)
 				scores = sorted(scores)
 
 				if scores in tested:
 					continue
 				tested.append(scores)
 
 				s = spread((i,j,k))
 
 				if (s < 2):
 					unsurps.append(scores)
 				elif (s == 2):
 					surps.append(scores)
 				else:
 					continue
 
 	return (unsurps, surps)
 
 def getbesttriplet(triplets):
 	best = None
 
 	for i in triplets:
 		if best:
 			if (bestresult(i) > bestresult(best)):
 				best = i
 		else:
 			best = i
 
 	return best
 	
 
 def getmulticombos(peeps):
 	"""
 		Return the best surprising and non-surprising possibility for
 		each person.
 	"""
 
 	ret = []
 
 	for p in peeps:
 		u,s = getcombos(p)
 
 		bestu = getbesttriplet(u)
 		bests = getbesttriplet(s)
 
 		ret.append((bestu, bests))
 
 	return ret
 
 def getbestresults(scores, best, numsur):
 	"""
 		Figure out the maximum number of people that could have gotten
 		a single score >= best.  Limited to choosing only numsur surprising
 		triplets.
 	"""
 
 	peeps = getmulticombos(scores)
 
 	count = 0
 	surcount = 0
 
 	for p in peeps:
 		if (bestresult(p[0]) >= best):
 			# unsurprising is good
 			count = count + 1
 		elif ((bestresult(p[1]) >= best) and (surcount < numsur)):
 			count = count + 1
 			surcount = surcount + 1
 
 	return count
 
 def process(test):
 	N = test['N']
 	S = test['S']
 	p = test['p']
 	t = test['t']
 
 	return getbestresults(t, p, S)
 
 data = readfile("B-small-attempt0.in")
 
 for i in xrange(data['T']):
 	test = data['tests'][i]
 
 	result = process(test)
 
 	print "Case #%d: %d" % (i+1, result)
