import sys
 
 sys.setrecursionlimit(9299999)
 
 def min_time(C, F, X, speed, nb_cookies):
 	if (X - nb_cookies) / speed < (X - (nb_cookies - C)) / (speed + F):
 		return (X - nb_cookies) / speed
 	elif nb_cookies >= C:
 		return min_time(C, F, X, speed + F, nb_cookies - C)
 	else:
 		return (C - nb_cookies) / speed + min_time(C, F, X, speed, C)
 
 T = int(raw_input())
 for i in range(T):
 	C, F, X = map(float, raw_input().split())
 	print 'Case #%d: %f' % (i + 1, min_time(C, F, X, 2, 0))
