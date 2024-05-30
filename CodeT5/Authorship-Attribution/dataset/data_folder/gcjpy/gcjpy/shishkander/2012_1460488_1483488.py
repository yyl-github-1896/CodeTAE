#!/usr/bin/env python
 import cPickle, time
 F = {}
 # to compute F:
 def f(x, _x, _min, _max):
     if x < 10: 
         #raise StopIteration
         return set()
     l = len(str(x)) -1
     k = 10**l
     res = set()
     res.add(_x)
     for i in xrange(l):
         x = (x % 10) * k + x/10
         if _min <= x <= _max and _x < x:
             res.add(x)
     res.remove(_x)
     if res:
         #print _x, "=>", res
         F[_x] = sorted(res)
     return res
 
 def compute_F(B):
     for i in xrange(0, B+1):
         f(i,i, 0, B+1)
     with open("picle",'wb') as _file:
         cPickle.dump( F, _file)
 
 #print "start", time.time()
 #compute_F(2000000)
 #print "end  ", time.time()
 
 
 t_start = time.time()
 print "loading..."
 with open("picle",'rb') as _file:
     F = cPickle.load(_file)
 print "done in %.2fs" % (time.time() - t_start)
 print "loaded F with %i keys" % len(F)
 
 def case(A, B):
     print "XXXXXXXXX ", A, B
     res = 0
     res2 = 0
     for i in xrange(A, B):
         l = F.get(i, [])
         #l = sorted(f(i,i,A,B))
         #res += len(l)
         #l1 = sorted(F.get(i,[]))
         #if l != l1:
         #    print i, l, l1
 
         for x in l:
            if x <= B:
                res += 1
     return res
 
 def solve(fin, fout):
     T = int(fin.readline())
     for t in xrange(T):
         A, B = map(int, fin.readline().strip().split(" "))
         assert A <= B
         fout.write("Case #%i: %i\n" % (t+1, case(A,B)) )
     return True
 
 if __name__ == "__main__":
     import sys
     with open(sys.argv[1],'r') as fin:
         with open(sys.argv[2], 'w') as fout:
             solve(fin, fout)
