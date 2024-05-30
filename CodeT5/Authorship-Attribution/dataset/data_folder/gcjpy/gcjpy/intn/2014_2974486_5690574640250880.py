#!/usr/bin/env python
 import sys
 
 def put_mines_last_step(R, C, M, grid):
 	if M == 0:
 		return
 	R -= 1
 	C -= 1
 	grid[R][C] = '*'
 	M -= 1
 	r = R - 1
 	c = C - 1
 	while M > 0:
 		if r > c:
 			grid[r][C] = '*'
 			r -= 1
 		else:
 			grid[R][c] = '*'
 			c -= 1
 		M -= 1
 
 def put_mines(R, C, M, grid):
 	if R > C:
 		if M < C:
 			put_mines_last_step(R, C, M, grid)
 			return
 		for i in range(C):
 			grid[R - 1][i] = '*'
 		put_mines(R - 1, C, M - C, grid)
 		return
 	if M < R:
 		put_mines_last_step(R, C, M, grid)
 		return
 	for i in range(R):
 		grid[i][C - 1] = '*'
 	put_mines(R, C - 1, M - R, grid)
 	return
 
 def process(R, C, M):
 	rlt = ''
 	grid = []
 	for i in range(R):
 		grid.append(['.'] * C)
 	put_mines(R, C, M, grid)
 	if not C == 1:
 		for i in range(R):
 			if not grid[i][0] == '.':
 				break
 			if not grid[i][1] == '.':
 				return '\nImpossible'
 	if not R == 1:
 		for i in range(C):
 			if not grid[0][i] == '.':
 				break
 			if not grid[1][i] == '.':
 				return '\nImpossible'
 	grid[0][0] = 'c'
 	for i in grid:
 		rlt += '\n' + ''.join(i)
 	return rlt
 
 input_file = open(sys.argv[1], 'r')
 T = int(input_file.readline())
 for i in range(T):
 	(R, C, M) = map(int, input_file.readline().split())
 	print 'Case #%d:' % (i + 1), process(R, C, M)
