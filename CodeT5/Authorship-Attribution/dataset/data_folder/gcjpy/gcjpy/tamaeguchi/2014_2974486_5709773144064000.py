#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem B. Cookie Clicker Alpha
 # https://code.google.com/codejam/contest/2974486/dashboard#s=p1
 #
 
 import sys
 import itertools
 
 
 def solve(C, F, X):
     def needtime(cookies, farm):
         speed = 2.0 + F * farm
         return cookies / speed
 
     farm = 0
     pasttime = 0
     while True:
         complete = needtime(X, farm)
         nextfarm = needtime(C, farm)
         nextchallenge = needtime(X, farm + 1)
         if complete <= nextfarm + nextchallenge:
             return pasttime + complete
         pasttime += nextfarm
         farm += 1
 
 
 def main(IN, OUT):
     T = int(IN.readline())
     for index in range(T):
         C, F, X = map(float, IN.readline().split())
         OUT.write('Case #%d: %.7f\n' % (index + 1, solve(C, F, X)))
 
 
 def makesample(maxC=500, maxF=4, maxX=2000, T=100):
     import random
     print T
     for index in range(T):
         print ' '.join('{0}'.format(random.randint(10000, maxvalue * 10000) / 10000.0)
                        for maxvalue in (maxC, maxF, maxX))
 
 
 if __name__ == '__main__':
     if '-makesample' in sys.argv[1:]:
         makesample()
     else:
         main(sys.stdin, sys.stdout)
 
