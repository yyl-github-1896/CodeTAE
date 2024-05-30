import math
 
 f = open('csmall.in','r')
 out = open('out3.txt','w')
 inp = [[int(n) for n in s.split()] for s in f.readlines()]
 count = 1
 
 for e in inp[1:len(inp)]:
     interval = xrange(e[0],e[1]+1)
     exp = xrange(1, int(math.log(interval[-1],10))+1)
     skip = []
     pairs = []
     for i in interval:
         if str(i)[::-1] == str(i):
             continue
         for j in exp:
             val = int(str(i%10**j)+str(i/10**j))
             if val in skip:
                 continue
             elif val >= interval[0] and val <= interval[-1] and not val == i:
                 skip.append(i)
     out.write('Case #'+str(count)+': '+str(len(skip))+'\n')
     count += 1
 
 f.close()
 out.close()
