
 input_file = 'A-small-attempt0.in'
 output_file = 'a_out'
 
 googlerese = ''.join([
 	'ejp mysljylc kd kxveddknmc re jsicpdrysi',
 	'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd',
 	'de kr kd eoya kw aej tysr re ujdr lkgc jv',
 	'y qee', 'z'
 ])
 
 english = ''.join([
 	'our language is impossible to understand',
 	'there are twenty six factorial possibilities',
 	'so it is okay if you want to just give up',
 	'a zoo', 'q'
 ])
 
 alphabet = {}
 
 for g, e in zip(googlerese, english):
 	alphabet[g] = e
 
 lines = open(input_file, 'r').readlines()
 out = open(output_file, 'w')
 
 for i, l in enumerate(lines[1:]):
 	trans = 'Case #%i: %s' % (
 		i + 1, 
 		''.join([alphabet[c] for c in l if c in alphabet]))
 	print trans
 	out.write(trans + '\n')
 
 out.close()
 
 	
 	
 
