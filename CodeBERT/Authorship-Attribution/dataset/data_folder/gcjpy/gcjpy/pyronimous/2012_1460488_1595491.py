input_file = 'B-small-attempt1.in'
 output_file = 'b.out'
 
 
 def solvecase(inp):
 	data = [int(n) for n in inp.split()]
 	N, S, p = data[0:3]
 	if p == 0:
 		return N
 	t = data[3:]
 	ret = 0
 	for br in t:
 		d, r = br / 3, br % 3
 		if br == 0 or p - d > 2:
 			continue
 		if (d >= p) or (r and (d + 1) >= p):
 			ret += 1
 		elif S and (d + max(r, 1)) >= p:
 			ret += 1
 			S -= 1
 	return ret
 
 lines = open(input_file, 'r').readlines()
 out = open(output_file, 'w')
 
 for i, l in enumerate(lines[1:]):
 	sout = 'Case #%i: %i' % (i + 1, solvecase(l))
 	print sout
 	out.write(sout + '\n')
 
 out.close()
