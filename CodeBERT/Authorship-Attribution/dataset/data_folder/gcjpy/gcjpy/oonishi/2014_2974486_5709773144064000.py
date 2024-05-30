# coding: cp932
 
 
 lines = iter('''
 5
 30.0 1.0 2.0
 30.0 2.0 100.0
 30.50000 3.14159 1999.19990
 500.0 4.0 2000.0
 100.0 1.0 100000.0
 '''.splitlines(False)[1:])
 
 lines = iter(open(r'B-small-attempt0.in').readlines(False))
 
 caseCnt = int(next(lines))
 
 for case in range(1, caseCnt+1):
 	C, F, X = map(float, next(lines).split())
 	
 	v = 2.0
 	total = 0.0
 	goal = X/v
 	while 1:
 		farm = C/v + total
 		if farm >= goal:
 			answer = goal
 			break
 		v += F
 		total = farm
 		if goal > X/v + total:
 			goal = X/v + total	
 	print('Case #%d: %0.6lf'%(case, answer))
 	#import pdb;pdb.set_trace()
 	
 
