# coding: cp932
 
 
 lines = iter('''
 4
 1
 0.5
 0.6
 2
 0.7 0.2
 0.8 0.3
 3
 0.5 0.1 0.9
 0.6 0.4 0.3
 9
 0.186 0.389 0.907 0.832 0.959 0.557 0.300 0.992 0.899
 0.916 0.728 0.271 0.520 0.700 0.521 0.215 0.341 0.458
 '''.splitlines(False)[1:])
 import sys
 out = sys.stdout
 
 sys.setrecursionlimit(1500)
 
 lines = iter(open(r'D-small-attempt2.in').readlines(False))
 out = open('d-small.answer', 'w')
 
 #lines = iter(open(r'D-large.in').readlines(False))
 #out = open('d-large.answer', 'w')
 
 caseCnt = int(next(lines))
 
 def solve(N, K):
 	if N == [] and K == []:
 		return 0
 	if K[-1] > N[-1]:
 		return solve(N[:-1], K[1:])
 	else:
 		return solve(N[:-1], K[:-1])+1
 
 for case in range(1, caseCnt+1):
 	C = int(next(lines))
 	N = sorted(map(float, next(lines).split()), reverse=True)
 	K = sorted(map(float, next(lines).split()), reverse=True)
 	
 	# if C == 1:
 		# if N[0] > K[0]:
 			# print('Case #%d: 1 1'%case, file=out)
 		# else:
 			# print('Case #%d: 0 0'%case, file=out)
 		# continue
 	
 	W=0
 	k = 0
 	for i, n in enumerate(N):
 		if n < K[k]:
 			k += 1
 		else:
 			W += 1
 	
 	D = solve(N, K)
 	print('Case #%d: %d %d'%(case, D, W), file=out)
 	#import pdb;pdb.set_trace()
 	
