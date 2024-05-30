#!/usr/local/bin/python
 import sys, string
 
 
 #solve case function
 def solve_case(nm, lawn, case_number):
     zipped_lawn = zip(*lawn)
     for n in range(0, nm[0]):
         max_lawn_n = max(lawn[n])
         for m in range(0, nm[1]):
             max_lawn_m = max(zipped_lawn[m])
             if lawn[n][m] < max_lawn_n and lawn[n][m] < max_lawn_m:
                 print "Case #%d: NO" % case_number
                 return
 
     print "Case #%d: YES" % case_number
 
 
 #main
 def main():
     r = sys.stdin
     if len(sys.argv) > 1:
         r = open(sys.argv[1], 'r')
 
     total_cases = r.readline()
     for case_number in range(1, int(total_cases) + 1):
         nm = map(int, r.readline().strip().split(' '))
         lawn = []
         for n in range(0, nm[0]):
             lawn.append(map(int, r.readline().strip().split(' ')))
         solve_case(nm, lawn, case_number)
 
 # invoke main
 if __name__ == "__main__":
     main()