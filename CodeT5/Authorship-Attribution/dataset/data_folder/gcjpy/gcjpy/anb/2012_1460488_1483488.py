from sys import stdin
 
 def program():
 	T = int(stdin.readline())
 	for Ti in xrange(T):
 		A, B =  map(int, stdin.readline().rstrip().split(' '))
 		
 		ss = set()
 		for n in xrange(A, B + 1):
 			sn = str(n)
 			for i in xrange(1, len(sn)):
 				sm = sn[i:] + sn[:i]
 				if sm[0] != '0':
 					m = int(sm)
 					if m > n and m <= B:
 						ss.add((n, m))
 		
 		print 'Case #%d: %d' % (Ti + 1, len(ss))	
 	
 if __name__ == '__main__':
 	program()