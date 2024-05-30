from sys import stdin
 
 def get_mapping():
 	d = ord('a')
 	mapping = [ None ] * 26
 	inputs = [ 'ejp mysljylc kd kxveddknmc re jsicpdrysi', 
 		'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd', 
 		'de kr kd eoya kw aej tysr re ujdr lkgc jv' ]
 	outputs = [ 'our language is impossible to understand', 
 		'there are twenty six factorial possibilities', 
 		'so it is okay if you want to just give up' ]
 	
 	for i in xrange(len(inputs)):
 		input = inputs[i]
 		output = outputs[i]
 		for j in xrange(len(input)):
 			if input[j] == ' ':
 				continue
 			k = ord(input[j]) - d
 			if mapping[k] is None:
 				mapping[k] = output[j]
 	mapping[ord('q') - d] = 'z'
 	mapping[ord('z') - d] = 'q'
 				
 	return mapping
 			
 
 def program():
 	T = int(stdin.readline())
 	mapping = get_mapping()
 	d = ord('a')
 	for i in xrange(T):
 		s = stdin.readline().rstrip()
 		t = ''
 		
 		for ss in s:
 			if ss == ' ':
 				t += ' '
 			else:
 				t += mapping[ord(ss) - d]
 		print 'Case #%d: %s' % (i + 1, t)
 	
 if __name__ == '__main__':
 	program()