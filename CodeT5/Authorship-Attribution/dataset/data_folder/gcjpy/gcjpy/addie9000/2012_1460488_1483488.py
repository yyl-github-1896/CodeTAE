#!/usr/bin/python
 import sys, string, math
 
 #solve case function
 def solve_case(min, max, case_number):
 	ans = 0
 
 	for candidate in range(min, max + 1):
 		candidate_str = str(candidate)
 		ignore = []
 		for rot in range(1, len(candidate_str)):
 			rot_candidate = int(candidate_str[rot:] + candidate_str[:rot])
 			if not rot_candidate in ignore:
 				if rot_candidate <= max and candidate < rot_candidate:
 					ans = ans + 1
 				ignore.append(rot_candidate)
 
 	print "Case #%d: %d" % (case_number, ans)
 
 #main
 r = sys.stdin
 
 if len(sys.argv) > 1:
 	r = open(sys.argv[1], 'r')
 
 total_cases = r.readline()
 for case_number in range(1, int(total_cases) + 1):
 	case = map(int, r.readline().rstrip().split(' '))
 	solve_case(case[0], case[1], case_number)
 
