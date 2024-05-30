input_file = 'C-small-attempt4.in'
 #input_file = 'c_sample.in'
 output_file = 'c.out'
 
 
 def solvecase(inp):
 	A, B = [int(n) for n in inp.split()]
 	
 	def shift(s):
 		return s[-1] + s[:-1]
 	
 	ret = 0
 	for n in range(A, B + 1):
 		sn = str(n)
 		sm = sn
 		rep = []
 		for i in range(len(sn) - 1):
 			sm = shift(sm)
 			if not (sm in rep) and (B >= int(sm) > n):
 				ret += 1
 				rep.append(sm)
 	return ret
 
 
 lines = open(input_file, 'r').readlines()
 out = open(output_file, 'w')
 
 for i, l in enumerate(lines[1:]):
 	sout = 'Case #%i: %i' % (i + 1, solvecase(l))
 	print sout
 	out.write(sout + '\n')
 
 out.close()
