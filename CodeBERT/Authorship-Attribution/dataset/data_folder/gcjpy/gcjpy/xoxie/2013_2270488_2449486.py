import sys
 
 f = open( sys.argv[1] )
 t = int(f.readline())
 
 t = 1
 l = f.readline()
 while l != "":
     n,m = [int(x) for x in l.split()]
     lawn = [ [int(x) for x in f.readline().split()] for y in range(n)]
 
     rowMax = [ max(x) for x in lawn ]
     colMax = [ max([x[y] for x in lawn]) for y in range(m) ]
 
     output = "YES"
 
     for i in range(n):
         for j in range(m):
             if lawn[i][j] < rowMax[i]:
                 if lawn[i][j] < colMax[j]:
                     output = "NO"
     
     print "Case #%s: %s"%(t,output)
     t += 1
     l = f.readline()
