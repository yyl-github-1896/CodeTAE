#!/usr/bin/env python
 
 FILE_NAME_BASE = 'A-small'
 NUM_PROCESSES = 0
 
 def findMapping(knowledge):
 	# Build Googlerese to English mapping from example text.
 	mapping = {}
 	for english, googlerese in knowledge:
 		assert len(english) == len(googlerese)
 		for engChar, gooChar in zip(english, googlerese):
 			if ord('a') <= ord(engChar) <= ord('z'):
 				assert ord('a') <= ord(gooChar) <= ord('z')
 				if gooChar in mapping:
 					assert mapping[gooChar] == engChar
 				else:
 					mapping[gooChar] = engChar
 			else:
 				assert engChar == gooChar
 
 	# If one letter is not be specified in the example text, we can still
 	# complete the mapping.
 	alphabet = set(chr(i) for i in xrange(ord('a'), ord('z') + 1))
 	gooMissing = alphabet - set(mapping.iterkeys())
 	engMissing = alphabet - set(mapping.itervalues())
 	assert len(gooMissing) == len(engMissing)
 	if len(gooMissing) == 1:
 		gooChar, = gooMissing
 		engChar, = engMissing
 		mapping[gooChar] = engChar
 	else:
 		assert len(gooMissing) == 0
 
 	# Convert completed mapping to Python translate table.
 	assert len(mapping) == 26, mapping
 	return ''.join(mapping.get(chr(i), chr(i)) for i in xrange(256))
 
 def parse(inp):
 	return inp.readline().rstrip('\n'),
 
 def solve(line):
 	return line.translate(mapping)
 
 knowledge = (
 	( 'our language is impossible to understand',
 	  'ejp mysljylc kd kxveddknmc re jsicpdrysi' ),
 	( 'there are twenty six factorial possibilities',
 	  'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd' ),
 	( 'so it is okay if you want to just give up',
 	  'de kr kd eoya kw aej tysr re ujdr lkgc jv' ),
 	( 'a zoo',
 	  'y qee' ),
 	)
 
 mapping = findMapping(knowledge)
 
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
