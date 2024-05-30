#!/usr/bin/env python
 
 
 import cPickle
 
 D1 = {} # no suprize
 D2 = {} # surprize
 for i in xrange(0, 31):
     D1[i] = D2[i] = -1
 
 def precompute():
     for a in xrange(0, 11):
         for b in xrange(a, min(a+3,11)):
             for c in xrange(b, min(a+3,11)):
                 t = a+b+c
                 assert a <= b <= c <= a+2 and c <= 11
                 if c < a+2:
                     D1[t] = max(D1[t], c)
                 else: # that is, c == a+2, we have a suprize
                     D2[t] = max(D2[t], c)
 
 #    for k in D1:
 #        print k, D2[k] - D1[k]
 
 precompute()
 #import cPickle
 #with open("prec","wb") as f:
 #    cPickle.dump((D1, D2), f )
 #print D1, D2
 
 def case(S, P, ts):
     res_n = 0
     res_s = 0
     for t in ts:
         if D1[t] >= P:
             res_n+=1
         elif D2[t]>=P:
             res_s+=1
     return (res_n + min(res_s, S))
 
 
 def solve(fin, fout):
     T = int(fin.readline())
     for t in xrange(T):
         nums = map(int, fin.readline().strip().split(" "))
         N, S, P = nums[:3]
         ts = nums[3:]
         assert len(ts) == N    
         fout.write("Case #%i: %i\n" % (t+1, case(S,P,ts)) )
     return True
 
 if __name__ == "__main__":
     import sys
     with open(sys.argv[1],'r') as fin:
         with open(sys.argv[2], 'w') as fout:
             solve(fin, fout)
