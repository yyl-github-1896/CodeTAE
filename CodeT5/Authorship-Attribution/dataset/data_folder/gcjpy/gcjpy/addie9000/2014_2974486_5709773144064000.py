#!/usr/bin/python
 import sys, string
 
 #solve case function
 def solve_case(c, f, x, case_number):
     rate = 2.0
     time = 0.0
     rest = x
     while True:
         time_to_c = c / rate
         time_to_x = rest / rate
         if time_to_c < time_to_x:
             time_to_x_with_boost = time_to_c + (rest / (rate + f))
             if time_to_x_with_boost < time_to_x:
                 rate += f
                 time += time_to_c
             else:
                 break
         else:
             break
     time += rest / rate
     print "Case #%d: %.7f" % (case_number, time)
 
 #main
 r = sys.stdin
 
 if len(sys.argv) > 1:
     r = open(sys.argv[1], 'r')
 
 total_cases = r.readline()
 for case_number in range(1, int(total_cases) + 1):
     values = map(float, r.readline().split(' '))
     solve_case(values[0], values[1], values[2], case_number)
