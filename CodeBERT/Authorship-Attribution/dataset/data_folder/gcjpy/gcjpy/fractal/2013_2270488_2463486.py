#! /usr/bin/python
 
 T = input()
 
 for n in range(1, T+1):
 
     A, B = raw_input().split()
     A, B = int(A), int(B)
 
     j = 0
     for i in range(A, B+1):
         s = str(i)
         m = int(i**.5)
         if s[-1] in ["1", "4", "5", "6", "9"] and \
                 (s == "".join(reversed(s))) and \
                 m**2 == i:
             s = str(m)
             if s == "".join(reversed(s)):
                 j += 1
 
 
     print "Case #%d: %d" % (n, j)
