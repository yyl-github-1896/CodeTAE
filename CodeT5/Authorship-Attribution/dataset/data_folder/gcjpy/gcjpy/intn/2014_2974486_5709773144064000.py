#!/usr/bin/env python
 import sys
 
 
 def process(C, F, X):
 	speed = 2.0
 	time = 0.0
 	while True:
 		if C / speed + X / (speed + F) > X / speed:
 			time += X / speed
 			break
 		time += C / speed
 		speed += F
 	return round(time, 7)
 
 input_file = open(sys.argv[1], 'r')
 T = int(input_file.readline())
 for i in range(T):
 	(C, F, X) = map(float, input_file.readline().split())
 	print 'Case #%d:' % (i + 1), process(C, F, X)
