T = int(raw_input().strip())
 
 for i in xrange(T):
 	C, F, X = map(float, raw_input().strip().split(' '))
 	best = X / 2.0
 	c_sum = 0
 	factories = 1
 	n_sum = c_sum + C / (2.0 + (factories - 1) * F)
 	while n_sum + X / (2.0 + factories * F) < best:
 		best = n_sum + X / (2.0 + factories * F)
 		c_sum = n_sum
 		factories += 1
 		n_sum = c_sum + C / (2.0 + (factories - 1) * F)
 
 	print "Case #%s: %s" % (i + 1, best)
