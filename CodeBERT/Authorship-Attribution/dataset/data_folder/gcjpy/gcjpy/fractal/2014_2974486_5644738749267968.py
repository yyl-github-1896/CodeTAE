#! /usr/bin/python3
 
 T = int(input())
 
 for n in range(1, T+1):
     blocks = int(input())
     naomi = [ int(float(a)*(10**5)) for a in input().split() ]
     ken = [ int(float(a)*(10**5)) for a in input().split() ]
 
     naomi.sort()
     ken.sort()
     dcwar = blocks
     war = 0
     i = 0
     j = 0
     while i<blocks and j<blocks:
         if ken[i] > naomi[j]:
             dcwar -= 1
         else:
             i += 1
         j += 1
     i = 0
     j = 0
     while i<blocks and j<blocks:
         if ken[i] < naomi[j]:
             war += 1
         else:
             j += 1
         i += 1
 
     print("Case #%d: %d %d" % (n, dcwar, war))
         
 
