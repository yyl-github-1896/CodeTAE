#!/usr/bin/env python
 
 FILE_NAME_BASE = 'C-small-attempt0'
 NUM_PROCESSES = 0
 
 def parse(inp):
 	a, b = (int(x) for x in inp.readline().split())
 	return a, b
 
 def solve(a, b):
 	count = 0
 	for i in xrange(a, b):
 		s = str(i)
 		recycled = set()
 		for d in xrange(1, len(s)):
 			r = s[d : ] + s[ : d]
 			if i < int(r) <= b:
 				recycled.add(r)
 		count += len(recycled)
 	return count
 
 if __name__ == '__main__':
 	inp = open(FILE_NAME_BASE + '.in.txt', 'r')
 	numCases = int(inp.readline())
 	if NUM_PROCESSES == 0:
 		results = [
 			solve(*parse(inp))
 			for _ in range(numCases)
 			]
 	else:
 		from multiprocessing import Pool
 		pool = Pool(NUM_PROCESSES)
 		results = [
 			pool.apply_async(solve, parse(inp))
 			for _ in range(numCases)
 			]
 	inp.close()
 	out = open(FILE_NAME_BASE + '.out.txt', 'w')
 	for case, result in enumerate(results):
 		value = result if NUM_PROCESSES == 0 else result.get()
 		out.write('Case #%d: %s\n' % (case + 1, value))
 		out.flush()
 	out.close()
