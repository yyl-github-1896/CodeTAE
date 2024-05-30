#!/usr/bin/env python
 
 from itertools import count
 import sys
 
 
 def next_lawn(stream):
     init = stream.readline()
     if not init:
         return None
 
     N, _ = map(int, init.split())
     lawn = []
     for i in range(N):
         line = stream.readline()
         lawn.append([int(x) for x in line.split()])
     return lawn
 
 
 def test_hor(lawn, i, j):
     me = lawn[i][j]
     return all(lawn[i][col] <= me for col in range(len(lawn[i])))
 
 
 def test_ver(lawn, i, j):
     me = lawn[i][j]
     return all(lawn[row][j] <= me for row in range(len(lawn)))
 
 
 def test_square(lawn, i, j):
     return test_hor(lawn, i, j) or test_ver(lawn, i, j)
 
 
 def is_possible(lawn):
     return all(test_square(lawn, i, j) for i in range(len(lawn))
                for j in range(len(lawn[i])))
 
 
 def main():
     with open('B-small-attempt0.in', encoding='utf-8') as f:
         f.readline()            # Skip the first line
 
         for i in count(1):
             lawn = next_lawn(f)
             if lawn is None:
                 break
             ans = is_possible(lawn)
             print('Case #{}: {}'.format(i, 'YES' if ans else 'NO'))
         
 
 main()
