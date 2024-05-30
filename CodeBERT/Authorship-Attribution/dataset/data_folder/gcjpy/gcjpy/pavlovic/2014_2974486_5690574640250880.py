import sys
 
 def generate_matrix(r, c, char):
 	mat = [[char for i in range(c)] for j in range(r)]
 	return mat
 	
 def merge(mat1, mat2):
 	for i in range(len(mat1)):
 		for j in range(len(mat1[i])):
 			mat2[i][j] = mat1[i][j]
 	return mat2
 
 def solve(r, c, m):
 	if 0 == m:
 		mat = generate_matrix(r, c, '.')
 		mat[0][0] = 'c'
 		return mat
 		
 	f = r * c - m
 	
 	if 0 == f:
 		return False
 		
 	if 1 == f:
 		mat = generate_matrix(r, c, '*')
 		mat[0][0] = 'c'
 		return mat
 		
 	if 1 == min(r, c):
 		mat = generate_matrix(r, c, '*')
 		for i in range(f):
 			mat[0 if 1 == r else i][0 if 1 == c else i] = '.'
 		mat[0][0] = 'c'
 		return mat
 
 	if 2 == min(r, c):
 		if (0 != f % 2) or (2 == f):
 			return False
 		mat = generate_matrix(r, c, '*')
 		for i in range(f // 2):
 			mat[0 if 2 == r else i][0 if 2 == c else i] = '.'
 			mat[1 if 2 == r else i][1 if 2 == c else i] = '.'
 		mat[0][0] = 'c'
 		return mat
 		
 	if (3 == r) and (3 == c):
 		if (4 == f) or (6 == f):
 			mat = generate_matrix(r, c, '*')
 			for i in range(f // 2):
 				mat[0][i] = '.'
 				mat[1][i] = '.'
 			mat[0][0] = 'c'
 			return mat
 		if 8 == f:
 			mat = generate_matrix(r, c, '.')
 			mat[2][2] = '*'
 			mat[0][0] = 'c'
 			return mat
 		return False
 		
 	rows_to_reduce = min(r - 3, m // c)
 	if 0 < rows_to_reduce:
 		res = solve(r - rows_to_reduce, c, m - rows_to_reduce * c)
 		if False == res:
 			return False
 		mat = merge(res, generate_matrix(r, c, '*'))
 		return mat
 		
 	cols_to_reduce = min(c - 3, m // r)
 	if 0 < cols_to_reduce:
 		res = solve(r, c - cols_to_reduce, m - cols_to_reduce * r)
 		if False == res:
 			return False
 		mat = merge(res, generate_matrix(r, c, '*'))
 		return mat
 	
 	mat = generate_matrix(r, c, '.')
 	for i in range(min(m, r - 2)):
 		mat[r - i - 1][c - 1] = '*'
 	if m == r - 1:
 		mat[r - 1][c - 2] = '*'
 	mat[0][0] = 'c'
 	return mat
 			
 
 t = int(sys.stdin.readline().strip())
 
 for i in range(t):
 	print "Case #" + str(i + 1) + ":"
 
 	r, c, m = [int(i) for i in sys.stdin.readline().strip().split()]
 	
 	res = solve(r, c, m)
 	
 	if False == res:
 		print "Impossible"
 	else:
 		for i in range(r):
 			for j in range(c):
 				sys.stdout.write(res[i][j])
 			print
