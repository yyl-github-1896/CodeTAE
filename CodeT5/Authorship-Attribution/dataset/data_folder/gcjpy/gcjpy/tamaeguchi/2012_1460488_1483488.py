#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem C. Recycled Numbers
 # http://code.google.com/codejam/contest/1460488/dashboard#s=p2
 #
 
 import sys
 import string
 
 
 def solve(A, B):
 	# Given integers A and B with the same number of digits
 	# なのでAとBは同じケタ数のはず
 	top = str(B)[0]
 
 	count = 0
 	for n in xrange(A, B):		# n=B のケースは検証不要(n < m <= B になりえない)
 		digit = str(n)
 		found = set()
 		for index in range(1, len(digit)):
 			if digit[index] < digit[0]:
 				# m の先頭が n の先頭より小さい → n < m にならない
 				continue
 			if digit[index] > top:
 				# m の先頭が B の先頭より大きい → m <= B にならない
 				continue
 
 			m = int(digit[index:] + digit[:index])
 			if n < m and m <= B and m not in found:
 				found.add(m)		# distinct 判定(見つけたものは除外)
 				count += 1
 				#print n, m
 	return count
 
 
 def main(IN, OUT):
 	N = int(IN.readline())
 	for index in range(N):
 		A, B = map(int, IN.readline().strip().split())
 		OUT.write('Case #%d: %d\n' % (index + 1, solve(A, B)))
 
 
 def makesample(ABmax=2000000, T=50):
 	import random
 	print T
 	for index in range(T):
 		A = random.randint(1, ABmax)
 		B = random.randint(A, ABmax)
 		print A, B
 
 
 if __name__ == '__main__':
 	if '-makesample' in sys.argv[1:]:
 		makesample()
 	else:
 		main(sys.stdin, sys.stdout)
 
