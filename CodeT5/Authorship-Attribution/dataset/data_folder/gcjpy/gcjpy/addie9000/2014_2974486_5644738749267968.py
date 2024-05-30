# !/usr/bin/python
 import sys, string
 
 #solve case function
 def solve_case(naomi_blocks, ken_blocks, case_number):
     naomi_blocks_for_deceitful = naomi_blocks[:]
     ken_blocks_for_deceitful = ken_blocks[:]
     deceitful_war_point = 0
     while len(naomi_blocks_for_deceitful) > 0:
         naomi_call = naomi_blocks_for_deceitful.pop(0)
         min_ken_call = ken_blocks_for_deceitful[0]
         if naomi_call < min_ken_call:
             naomi_call = ken_blocks_for_deceitful[-1] - 0.000001
         else:
             # Naomi may call the same kg many times but Ken should not realize it ;)
             # The important point is that she must call heavier than Ken's max.
             naomi_call = ken_blocks_for_deceitful[-1] + 0.000001
 
         ken_candidate = filter(lambda x: x > naomi_call, ken_blocks_for_deceitful)
         if len(ken_candidate) > 0:
             ken_call = ken_blocks_for_deceitful.pop(ken_blocks_for_deceitful.index(ken_candidate.pop(0)))
         else:
             ken_call = ken_blocks_for_deceitful.pop(0)
 
         if naomi_call > ken_call:
             deceitful_war_point += 1
 
     war_point = 0
     while len(naomi_blocks) > 0:
         naomi_call = naomi_blocks.pop(0)
         ken_candidate = filter(lambda x: x > naomi_call, ken_blocks)
         if len(ken_candidate) > 0:
             ken_call = ken_blocks.pop(ken_blocks.index(ken_candidate.pop(0)))
         else:
             ken_call = ken_blocks.pop(0)
 
         if naomi_call > ken_call:
             war_point += 1
 
     print "Case #%d: %d %d" % (case_number, deceitful_war_point, war_point)
 
 #main
 r_file = sys.stdin
 
 if len(sys.argv) > 1:
     r_file = open(sys.argv[1], 'r')
 
 total_cases = r_file.readline()
 for case_number in range(1, int(total_cases) + 1):
     r_file.readline()
     n_values = map(float, r_file.readline().split(' '))
     k_values = map(float, r_file.readline().split(' '))
     solve_case(sorted(n_values), sorted(k_values), case_number)
 
