#!/usr/bin/python3
 
 import sys
 
 ncases = int(sys.stdin.readline().strip())
 
 def read_arrangement():
     arr = []
     for row in range(0,4):
         arr.append(sys.stdin.readline().strip().split(' '))
     return arr
 
 for t in range(1, ncases+1):
     answer1 = int(sys.stdin.readline().strip())
     arrang1 = read_arrangement()
     answer2 = int(sys.stdin.readline().strip())
     arrang2 = read_arrangement()
 
     row1 = arrang1[answer1-1]
     row2 = arrang2[answer2-1]
 
     intersect = set(row1) & set(row2)
 
     if len(intersect) == 1:
         print("Case #{0}: {1}".format(t, intersect.pop()))
     elif len(intersect) == 0:
         print("Case #{0}: Volunteer cheated!".format(t))
     else:
         print("Case #{0}: Bad magician!".format(t))
