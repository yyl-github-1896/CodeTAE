import sys
 
 def is_sym( number ):
 	num_str = str( number )
 	num_len = len( num_str )
 	half_len = int( num_len / 2 )
 	end = num_str[-half_len:]
 	rev_end = end[::-1]
 	start = num_str[:half_len]
 	equal = rev_end == start 
 	return equal
 
 f = open( 'palindromes.out' )
 
 numbers = [ int(x) for x in f.read().split() ]
 
 numCases = input()
 for case in range( 1, numCases + 1 ):
 	min, max = [ int(x) for x in raw_input().split() ]
 	count = 0
 	for number in numbers:
 		if min <= number and max >= number:
 			count += 1
 
 	print 'Case #' + str( case ) + ': ' + str( count )
