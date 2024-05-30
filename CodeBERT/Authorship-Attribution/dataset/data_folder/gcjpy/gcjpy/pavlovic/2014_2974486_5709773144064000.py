import sys
 import math
 
 def calculate_time(c, f, x, num_farms):
 	t = 0.0
 	rate = 2.0
 	for i in range(num_farms):
 		t += c / rate
 		rate += f
 		
 	t += x / rate
 	return t	
 
 t = int(sys.stdin.readline().strip())
 
 for i in range(t):
 	print "Case #" + str(i + 1) + ":",
 
 	(c, f, x) = [float(i) for i in sys.stdin.readline().strip().split()]
 	
 	if x <= c:
 		t = calculate_time(c, f, x, 0)
 	else:
 		opt_rate = f * (x - c) / c
 		num_farms = (opt_rate - 2) / f
 		t1 = calculate_time(c, f, x, int(math.floor(num_farms)))
 		t2 = calculate_time(c, f, x, int(math.ceil(num_farms)))
 
 		t = min(t1, t2)
 		
 	print "%.7f" % t
