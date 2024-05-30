import sys
 
 translation = { 'a' : 'y', 'b' : 'h', 'c' : 'e', 'd' : 's', 'e' : 'o', 'f' : 'c', 'g' : 'v', 'h' : 'x',
 'i' : 'd', 'j' : 'u', 'k' : 'i', 'l' : 'g', 'm' : 'l', 'n' : 'b', 'o' : 'k', 'p' : 'r', 'q' : 'z', 'r' : 't',
  's' : 'n', 't' : 'w', 'u' : 'j', 'v' : 'p', 'w' : 'f', 'x' : 'm', 'y' : 'a', 'z' : 'q', ' ' : ' ' }
 
 #words = 'ejp mysljylc kd kxveddknmc re jsicpdrysi rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd de kr kd eoya kw aej tysr re ujdr lkgc jv'
 
 numCases = input()
 for case in range( 1, numCases + 1 ):
 	words = raw_input()
 	output = ''
 	
 	for letter in words:
 		output = output + translation[letter]
 
 	print 'Case #' + str( case ) + ': ' + output
