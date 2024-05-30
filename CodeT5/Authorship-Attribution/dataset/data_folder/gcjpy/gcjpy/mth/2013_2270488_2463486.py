#!/usr/bin/env python
 
 from math import sqrt
 
 FILE_NAME_BASE = 'C-small-attempt0'
 NUM_PROCESSES = 0
 MEM_LIMIT_GB = 1.5 # per worker process
 RECURSION_LIMIT = 1000
 
 def parse(inp):
 	a, b = (int(x) for x in inp.readline().split())
 	return a, b
 
 def isFair(x):
 	l1 = list(str(x))
 	l2 = list(l1)
 	l2.reverse()
 	return l1 == l2
 
 def solve(a, b):
 	c = 0
 	for i in xrange(a, b + 1):
 		r = int(sqrt(i))
 		if r * r == i and isFair(i) and isFair(r):
 			c += 1
 
 	return str(c)
 
 def main():
 	import sys
 	sys.setrecursionlimit(RECURSION_LIMIT)
 
 	import resource
 	soft, hard = resource.getrlimit(resource.RLIMIT_AS)
 	resource.setrlimit(resource.RLIMIT_AS, (MEM_LIMIT_GB * 1024 ** 3, hard))
 
 	inp = open(FILE_NAME_BASE + '.in', 'r')
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
 	out = open(FILE_NAME_BASE + '.out', 'w')
 	for case, result in enumerate(results):
 		value = result if NUM_PROCESSES == 0 else result.get()
 		out.write('Case #%d: %s\n' % (case + 1, value))
 		out.flush()
 	out.close()
 
 if __name__ == '__main__':
 	main()
