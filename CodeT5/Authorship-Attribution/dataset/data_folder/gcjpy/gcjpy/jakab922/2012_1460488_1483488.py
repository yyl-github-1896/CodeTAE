from sys import argv
 from math import floor, log10
 
 def grab2(x):
 	if x < 2:
 		return 0
 	return x * (x - 1) / 2
 
 def solve(low, high):
 	was = [0 for i in range(low, high + 1)]
 	total = 0
 
 	for i in xrange(low, high + 1):
 		if was[i - low] == 0:
 			was[i - low] = 1
 			variations = set([i])
 			
 			if global_variations[i] != []:
 				for j in global_variations[i]:
 					if j >= low and j <= high:
 						was[j - low] = 1
 						variations.add(j)
 			else:
 				curr = i
 				clen = int(floor(log10(i)))
 				pow10 = pow(10, clen)
 				cgvariations = set(list(variations))
 				for i in range(clen):
 					pre = curr % 10
 					curr = pow10 * pre + (curr - (curr % 10)) / 10
 					if pre != 0 and curr not in variations and curr >= low and curr <= high:
 						variations.add(curr)
 						was[curr - low] = 1
 					if pre != 0 and curr < ma and curr not in cgvariations:
 						cgvariations.add(curr)
 
 				for cg in cgvariations:
 					global_variations[cg] = list(cgvariations)
 
 			total += grab2(len(variations))
 
 
 	return total
 
 f = open(argv[1], 'r')
 T = int(f.readline().strip('\n'))
 mi = 2000000
 ma = 1
 ab = []
 for i in range(T):
 	ab.append(map(int, f.readline().strip('\n').split(' ')))
 	if ab[-1][1] > ma:
 		ma = ab[-1][1]
 
 global_variations = [[] for i in range(ma + 2)]
 
 i = 1
 for x in ab:
 	print "Case #%s: %s" % (i, solve(x[0],x[1]))
 	i += 1