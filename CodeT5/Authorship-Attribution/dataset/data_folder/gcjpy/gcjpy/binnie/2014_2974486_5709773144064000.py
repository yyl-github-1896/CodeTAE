import sys
 from decimal import *
 
 f = open(sys.argv[1])
 T = int(f.readline())
 for test in range(T):
     data = f.readline().split()
     C = Decimal(data[0])
     F = Decimal(data[1])
     X = Decimal(data[2])
     curr_rate = Decimal(2)
     best_time = Decimal(10**100)
     curr_time = Decimal(0)
     while curr_time < best_time:
         poss_finish_time = curr_time + X / curr_rate
         if poss_finish_time < best_time:
             best_time = poss_finish_time
 
         curr_time += C / curr_rate
         curr_rate += F
 
     print "Case #%d: %.7f" % (test + 1, best_time)
