#!/usr/bin/env python
 
 FILE_NAME_BASE = 'B-small-attempt0'
 NUM_PROCESSES = 0
 MEM_LIMIT_GB = 1.5 # per worker process
 RECURSION_LIMIT = 1000
 
 def parse(inp):
 	rows, cols = (int(x) for x in inp.readline().split())
 	return tuple(
 		tuple(int(x) for x in inp.readline().split())
 		for row in xrange(rows)
 		),
 
 def solve(lawn):
 	#print lawn
 
 	rowMax = tuple(max(row) for row in lawn)
 	colMax = tuple(max(row[i] for row in lawn) for i in xrange(len(lawn[0])))
 	#print rowMax, colMax
 
 	def possible():
 		for y, row in enumerate(lawn):
 			for x, cell in enumerate(row):
 				h = min(rowMax[y], colMax[x])
 				if cell != h:
 					return False
 		return True
 
 	return 'YES' if possible() else 'NO'
 
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
