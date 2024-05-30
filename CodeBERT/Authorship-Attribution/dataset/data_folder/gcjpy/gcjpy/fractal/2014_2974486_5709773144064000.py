#! /usr/bin/python3
 
 T = int(input())
 
 for x in range(1, T+1):
     (C, F, X) = [float(y) for y in input().split()]
     totalsecs = 0
     cur_speed = 2
     while True:
         cur_time = X/cur_speed
         new_speed = cur_speed + F
         new_time = C/cur_speed + X/new_speed
         if new_time < cur_time:
             totalsecs += C/cur_speed
             cur_speed = new_speed
         else:
             totalsecs += cur_time
             break
     
     print("Case #%d: %.7f" % (x, totalsecs))
