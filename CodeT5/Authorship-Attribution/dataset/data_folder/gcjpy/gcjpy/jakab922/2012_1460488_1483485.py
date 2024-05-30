from sys import argv
 
 mapping = { "a": "y", "c": "e", "b": "h", "e": "o", "d": "s", "g": "v", "f": "c", "i": "d", "h": "x", "k": "i", "j": "u", "m": "l", "l": "g", "o": "k", "n": "b", "p": "r", "s": "n", "r": "t", "u": "j", "t": "w", "w": "f", "v": "p", "y": "a", "x": "m", "q": "z", "z": "q"}
 
 def translator(s):
 	ret = []
 	for c in s:
 		if ord(c) > 96 and ord(c) < 123:
 			ret.append(mapping[c])
 		else:
 			ret.append(c)
 
 	return ''.join(ret)
 
 f = open(argv[1], 'r')
 T = int(f.readline().strip('\n'))
 for i in range(T):
 	line = f.readline().strip('\n')
 	print "Case #%s: %s" % (i + 1, translator(line))