import sys
 
 
 def read_case(f):
 	return map(float, f.readline().split())
 
 
 def solve(C, F, X, rate=2.0):
 	accum = 0
 	while 1:
 		goal1 = X / rate
 	
 		farm = C / rate
 		goal2 = farm + (X / (rate + F))
 
 		if goal1 <= goal2:
 			return accum + goal1
 		else:
 			accum += farm
 			rate += F
 
 			
 def trunc(x, p=7):
 	m = 10 ** p
 	return round(x * m) / m
 
 
 def main():
 	fn = sys.argv[1]
 	with open(fn, encoding='utf-8') as f:
 		ncases = int(f.readline())
 		for case in range(1, ncases + 1):
 			C, F, X = read_case(f)
 			solution = solve(C, F, X)
 			print('Case #{}: {}'.format(case, trunc(solution)))
 
 
 if __name__ == '__main__':
 	main()
