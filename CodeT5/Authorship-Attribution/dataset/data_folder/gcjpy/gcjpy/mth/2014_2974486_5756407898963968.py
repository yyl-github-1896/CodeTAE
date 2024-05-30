#!/usr/bin/env python
 
 FILE_NAME_BASE = 'A-small-attempt0'
 NUM_PROCESSES = 0
 MEM_LIMIT_GB = 1.5 # per worker process
 RECURSION_LIMIT = 1000
 
 def parseBoard(inp):
 	rowSel, = (int(x) for x in inp.readline().split())
 	board = tuple(
 		tuple(int(x) for x in inp.readline().split())
 		for _ in xrange(4)
 		)
 	return board, rowSel - 1
 
 def parse(inp):
 	before, beforeSel = parseBoard(inp)
 	after, afterSel = parseBoard(inp)
 	return before, beforeSel, after, afterSel
 
 def solve(before, beforeSel, after, afterSel):
 	candidates = set(before[beforeSel]) & set(after[afterSel])
 
 	if len(candidates) == 0:
 		return "Volunteer cheated!"
 	elif len(candidates) == 1:
 		return candidates.pop()
 	else:
 		return "Bad magician!"
 
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
