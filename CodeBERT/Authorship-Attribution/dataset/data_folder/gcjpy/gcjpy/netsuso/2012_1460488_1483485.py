#!/usr/bin/python3
 
 import sys
 
 reverseMappings = {
 'a': 'y',
 'b': 'h',
 'c': 'e',
 'd': 's',
 'e': 'o',
 'f': 'c',
 'g': 'v',
 'h': 'x',
 'i': 'd',
 'j': 'u',
 'k': 'i',
 'l': 'g',
 'm': 'l',
 'n': 'b',
 'o': 'k',
 'p': 'r',
 'q': 'z',
 'r': 't',
 's': 'n',
 't': 'w',
 'u': 'j',
 'v': 'p',
 'w': 'f',
 'x': 'm',
 'y': 'a',
 'z': 'q',
 ' ': ' '
 }
 
 def reverse(string):
 	return ''.join([reverseMappings[c] for c in string])
 
 # Ignore number of tests
 sys.stdin.readline()
 
 casenum=0
 for line in sys.stdin:
 	casenum += 1
 	reversed = reverse(line.strip())
 	print("Case #%d: %s" % (casenum, reversed))
