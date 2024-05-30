import sys
 
 def recycle(num):
     x = str(num)
     recycles = []
     for ii in range(1, len(x)):
         recycles.append(x[ii:] + x[:ii])    
     return recycles
 
 f = open(sys.argv[1])
 T = int(f.readline())
 for t in range(T):
     A, B = map(int, f.readline().split())
     total = 0
     debugs = []
     for ii in range(A,B):
         recycles_ii = recycle(ii)
         recycles_ii = (filter(lambda x: int(x) > ii and int(x) <= B, recycles_ii))
         total += len(recycles_ii)
         for elem in recycles_ii:
             debugs.append((ii, int(elem)))   
     print "Case #%d:" % (t + 1), len(set(debugs))
