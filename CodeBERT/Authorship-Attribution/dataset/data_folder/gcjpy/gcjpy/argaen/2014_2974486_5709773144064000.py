t = int(raw_input())
 
 for case in range(t):
 
 	c, f, x = raw_input().split()
 	c = float(c)
 	f = float(f)
 	x = float(x)
 
 	t = 0
 	cps = 2.0
 	while c/cps < x/cps and t+x/cps > t+c/cps + x/(cps+f):
 		# print t, c/cps, x/cps
 		t += c/cps
 		cps += f
 		# raw_input()
 
 	t += x/cps
 
 	print 'Case #'+str(case+1)+':', t
