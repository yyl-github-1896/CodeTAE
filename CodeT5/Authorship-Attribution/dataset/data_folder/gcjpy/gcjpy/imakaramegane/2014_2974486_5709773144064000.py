# coding: utf-8
 import sys
 import os.path
 import itertools
 from itertools import groupby
 import math
 
 def debug(v):
     pass#print(v)
 
 def read(f):
     t = tuple(int(v) for v in f.readline().split())
     debug(t)
     return t
 
 def readf(f):
     t = tuple(float(v) for v in f.readline().split())
     debug(t)
     return t
 
 def answer(f, X, ans):
     out = "Case #{}: {}".format(X, ans)
     f.write(out)
     f.write("\n")
     print(out)
 
 
 
 def main(inf, outf):
     T, = read(inf)
     for casenmbr in range(1, T + 1):
         C, F, X = readf(inf)
 
         power = 2
         farmtime = round(C / power, 7)
         keikatime = 0
         totaltime = round(X / power, 7)
 
         while True:
             keikatime += farmtime
             power += F
             farmtime = round(C / power, 7)
             nokoritime = round(X / power, 7)
             if keikatime + nokoritime > totaltime:
                 break
             totaltime = keikatime + nokoritime
 
         answer(outf, casenmbr, totaltime)
 
 
 if __name__=="__main__":
     infname = sys.argv[1]
     outfname = os.path.splitext(infname)[0] + ".out"
     with open(infname, "r") as inf:
         with open(outfname, "w") as outf:
             main(inf, outf)
