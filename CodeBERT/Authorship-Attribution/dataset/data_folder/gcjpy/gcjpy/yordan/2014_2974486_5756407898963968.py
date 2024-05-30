# -*- coding: utf-8 -*-
 
 import sys
 
 
 def read_grid(f):
 	return [
 		[int(x) for x in line.split()]
 		for line in [f.readline() for _ in range(4)]
 	]
 
 def read_case(f):
 	answer1 = int(f.readline())
 	grid1 = read_grid(f)
 	answer2 = int(f.readline())
 	grid2 = read_grid(f)
 	return (grid1[answer1 - 1], grid2[answer2 - 1])
 
 
 def solve(r1, r2):
 	res = set(r1) & set(r2)
 	if len(res) == 0:
 		return 'Volunteer cheated!'
 	if len(res) == 1:
 		return list(res)[0]
 	return 'Bad magician!'
 
 
 
 def main():
 	fn = sys.argv[1]
 	with open(fn, encoding='utf-8') as f:
 		ncases = int(f.readline())
 		for case in range(1, ncases + 1):
 			row1, row2 = read_case(f)
 			solution = solve(row1, row2)
 			print('Case #{}: {}'.format(case, solution))
 
 
 if __name__ == '__main__':
 	main()