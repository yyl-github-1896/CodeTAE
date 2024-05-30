import sys
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())
     for _t in range(t):
         N = int(f.readline())
         Naomi = sorted([float(x) for x in f.readline().split()])
         Ken = sorted([float(x) for x in f.readline().split()])
         NMax = max(Naomi)
         DWScore = 0
         WScore = 0
         NaomiW = [x for x in Naomi]
         KenW = [x for x in Ken]
         for i in range(N):
             if(Naomi[-1] > Ken[-1]):
                 DWScore += 1
                 Naomi.pop()
                 Ken.pop()
             else:
                 Naomi.pop(0)
                 Ken.pop()
         for i in range(N):
             Na = NaomiW.pop(0)
             KWinners = [x for x in KenW if x > Na]
             if len(KWinners) > 0:
                 KenW.remove(KWinners[0])
             else:
                 KenW.pop(0)
                 WScore += 1
         print ("Case #" + str(_t+1) + ": " + str(DWScore) + " " + str(WScore))
     
 
