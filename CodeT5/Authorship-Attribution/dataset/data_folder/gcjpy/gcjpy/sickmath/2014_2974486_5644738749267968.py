f = open('input.in')
 g = open('output', 'w')
 
 T = int(f.readline()[:-1])
 
 for case in xrange(T) :
     N = int(f.readline()[:-1])
     Naomi = sorted(map(float, f.readline()[:-1].split()))
     Ken = sorted(map(float, f.readline()[:-1].split()))
     Ken2 = Ken[:]
     War, DWar = 0, 0
     for n in Naomi :
         if n > max(Ken) :
             Ken.pop(0)
             War += 1
         else :
             for i, k in enumerate(Ken) :
                 if k > n : break
             Ken.pop(i)
     Ken = Ken2
     for n in Naomi :
         if n < min(Ken) :
             Ken.pop(-1)
         else :
             Ken.pop(0)
             DWar += 1
     output = 'Case #' + str(case + 1) + ': ' + str(DWar) + ' ' + str(War)
     g.write(output + '\n')
     print output
 
 f.close()
 g.close()
