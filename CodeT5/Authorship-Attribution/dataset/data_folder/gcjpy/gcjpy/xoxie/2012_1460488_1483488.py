import sys
 from collections import deque
 
 if __name__ == "__main__":
     f = open( "C-small-attempt0.in.txt" )
     g = open( "output_small.txt", "w" )
 
     numcases = int(f.readline())
 
     caseI = 1
     line = f.readline()
     while line != "":
         A,B = [int(x) for x in line.split()]
 
         matched = [0]*(B+1)
         pairs = deque()
 
         for x in range(A,B+1):
             if matched[x]:
                 continue
             a = str(x)
             allcycle = deque()
             allcycle.append(x)
             for i in range(1,len(a)):
                 yL,yR = a[:i],a[i:]
                 y = int( yR+yL )
                 if y >= A and y <= B:
                     allcycle.append(y)
             allcycle = list(set(allcycle))
             allcycle.sort()
             for y in allcycle:
                 matched[y] = 1
             for i in range(len(allcycle)):
                 for j in range(i+1,len(allcycle)):
                     pairs.append( (allcycle[i],allcycle[j]) )
         g.write( "Case #%s: %s\n"%(caseI,len(pairs)) )
         line = f.readline()
         caseI += 1
     f.close()
     g.close()
