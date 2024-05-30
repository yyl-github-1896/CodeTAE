#!/usr/bin/env python
 
 FILE_NAME_BASE = 'D-small-attempt0'
 NUM_PROCESSES = 0
 MEM_LIMIT_GB = 1.5 # per worker process
 RECURSION_LIMIT = 1000
 
 from itertools import chain
 
 def parse(inp):
 	numBlocks, = (int(x) for x in inp.readline().split())
 	naomiBlocks = tuple(sorted(float(x) for x in inp.readline().split()))
 	kenBlocks = tuple(sorted(float(x) for x in inp.readline().split()))
 	assert len(naomiBlocks) == numBlocks
 	assert len(kenBlocks) == numBlocks
 	return naomiBlocks, kenBlocks
 
 def solve(naomiBlocks, kenBlocks):
 	numBlocks = len(naomiBlocks)
 
 	# greedy strategy for honest play:
 	# play the block that is heavier by the smallest margin (if you have one)
 	# ('honest' meaning sticking to the rules; 'fair' is something else)
 	kenPointsHonest = 0
 	naomiLowerBlocks = 0
 	for _, owner in sorted(chain(
 			((b, 'n') for b in naomiBlocks),
 			((b, 'k') for b in kenBlocks)
 			)):
 		if owner == 'n':
 			naomiLowerBlocks += 1
 		elif naomiLowerBlocks != 0:
 			naomiLowerBlocks -= 1
 			kenPointsHonest += 1
 	naomiPointsHonest = numBlocks - kenPointsHonest
 
 	# strategy for deceitful play:
 	# moves:
 	# + lie and win:
 	#   when Ken can't match the told number, he'll play his lightest block
 	#   so you can lie and win if you play a block heavier than his lightest
 	# + lie and lose:
 	#   name a weight just below Ken's heaviest block, forcing him to play that
 	# - truth and win:
 	#   when you play a block that is actually heavier than anything Ken has
 	#   is just a special case of lie and win
 	# - truth and lose:
 	#   never optimal
 	# optimal order of play:
 	#   always play your lightest block: if it can't win now, it can never win
 	#   in the future either, nor can it be more effective in the future than
 	#   pulling his current heaviest block
 	naomiLoIdx = 0
 	naomiHiIdx = numBlocks - 1
 	kenLoIdx = 0
 	kenHiIdx = numBlocks - 1
 	naomiPointsDeceit = 0
 	while naomiLoIdx <= naomiHiIdx:
 		assert naomiHiIdx - naomiLoIdx == kenHiIdx - kenLoIdx
 		naomiLo = naomiBlocks[naomiLoIdx]
 		#naomiHi = naomiBlocks[naomiHiIdx]
 		kenLo = kenBlocks[kenLoIdx]
 		#kenHi = kenBlocks[kenHiIdx]
 		if naomiLo > kenLo:
 			naomiPointsDeceit += 1
 			kenLoIdx += 1
 		else:
 			kenHiIdx -= 1
 		naomiLoIdx += 1
 
 	#print naomiBlocks
 	#print kenBlocks
 	#print
 
 	return '%d %d' % (naomiPointsDeceit, naomiPointsHonest)
 
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
