# coding: shift-jis
 
 import sys
 #f = file("test.in")
 #w = sys.stdout
 f = file("C-small-attempt0.in")
 w = file("answer.txt", "w")
 cnt = int(f.readline()[:-1])
 from math import log
 for no in range(cnt):
 	A, B = map(int, f.readline()[:-1].split())
 	
 	count = 0
 	for n in range(A, B):
 		d = int(log(n, 10))+1
 		s = set()
 		for e in range(1, d):
 			c = 10**e
 			r = (n % c)*10**(d-e)
 			b = n / c
 			if r+b>n and r+b<=B and (n, r+b) not in s:
 				s.add((n, r+b))
 				count += 1
 				
 	print>>w, "Case #%d:"%(no+1), count
 
 
