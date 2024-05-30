# coding: shift-jis
 
 import sys
 f = file("B-small-attempt0.in")
 #f = file("test.in")
 #w = sys.stdout
 w = file("answer.txt", "w")
 cnt = int(f.readline()[:-1])
 for no in range(cnt):
 	l = f.readline()[:-1].split()
 	T, s, p = map(int, l[:3])
 	ts = map(int, l[3:])
 	ns = p*3-2 if p*3-2 > 0 else 0
 	ss = p*3-4 if p*3-4 > 0 else 31
 	l = filter(lambda x: x<ns, ts)
 	c = min([len(filter(lambda x: x>=ss, l)), s])
 	
 	print>>w, "Case #%d:"%(no+1), T-len(l)+c
 
 
