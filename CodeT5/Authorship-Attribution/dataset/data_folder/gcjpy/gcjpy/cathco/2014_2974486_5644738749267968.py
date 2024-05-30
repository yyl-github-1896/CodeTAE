from copy import deepcopy
 import time
 
 def dwar(N, K):
   N = sorted(N)
   K = sorted(K)
   
   naomi = 0
   
   #if naomi can win then she should lose her lowest piece to do so
   #if kevin can win then he should lose his highest piece
   while len(N) > 0:
     # Naomi can win.
     if N[-1] > K[-1]:
       # Kevin loses highest piece.
       k = K.pop()
       # Naomi loses lowest piece necessary.
       for i, n in enumerate(N):
         if N[i] > k:
           choosen = i
           break
       del(N[choosen])
       naomi += 1
     # Naomi cannot win.
     else:
       # Naomi loses lowest piece.
       N = N[1:]
       k = K.pop()
   return naomi
 
 def war(N, K):
   N = sorted(N)
   K = sorted(K)
   
   naomi = 0
   while len(N) > 0:
     n = N.pop()
     chosen = None
     for i, k in enumerate(K):
       if k > n:
         chosen = i
         break
     if not chosen == None:
       del(K[chosen])
     else:
       naomi += 1
   return naomi
 
 T = int(raw_input())
 for t in range(T):
   _ = raw_input()
   N = map(float, raw_input().split())
   K = map(float, raw_input().split())
   
   print 'Case #%i: %i %i' % (t+1, dwar(N, K), war(N, K))
