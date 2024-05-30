#!/usr/bin/env python3
 
 from itertools import count
 from math import sqrt
 
 
 def next_range(stream):
     line = stream.readline()
     if not line:
         return None
     return [int(x) for x in line.split()]
 
 
 def is_palindrome(n):
     n = str(n)
     return all(n[i] == n[len(n)-1-i] for i in range(len(n) // 2))
 
 def mysqrt(n):
     """Return -1 if not an integer"""
     rt = int(sqrt(n))
     return rt if rt * rt == n else -1
 
 
 def is_fas(n):
     rt = mysqrt(n)
     return rt != -1 and is_palindrome(n) and is_palindrome(rt)
 
 
 def main():
     with open('C-small-attempt0.in', encoding='utf-8') as f:
         f.readline()
 
         for case in count(1):
             r = next_range(f)
             if r is None:
                 break
 
             cnt = 0
             for n in range(r[0], r[1] + 1):
                 if is_fas(n):
                     cnt += 1
 
             print('Case #{}: {}'.format(case, cnt))
 
 
 main()
