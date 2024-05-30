#!/usr/bin/python3
 
 import sys
 
 ncases = int(sys.stdin.readline().strip())
 
 for t in range(1, ncases+1):
     values = sys.stdin.readline().split()
     c = float(values[0])
     f = float(values[1])
     x = float(values[2])
     r = 2
 
     time = 0
 
     while True:
         tdirect = x/r
         tfactory = c/r + x/(r+f)
 
         if tdirect<tfactory:
             time += tdirect
             break
         else:
             time += c/r
             r += f
 
     print("Case #{0}: {1:.7f}".format(t, time))
