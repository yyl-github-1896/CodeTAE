import sys
 
 lines = sys.stdin.readlines()
 def parseCase(lines):
     dims = map(int,lines[0].split(" "))
     return dims[0]+1, [map(int,l.split(" ")) for l in lines[1:dims[0]+1]]
 
 
 def getCases(lines):
     i =0
     while i < len(lines):
         lines_used, case = parseCase(lines[i:])
         i += lines_used
         yield case
 
         
 cNum =0
 for c in getCases(lines[1:]):
     cNum += 1
     answer = None
     for i in range(len(c)):
         if answer: break
         for j in range(len(c[i])):
             if answer: break
             answer = max(c[i]) > c[i][j] and max([c[k][j] for k in range(len(c))]) > c[i][j]
     print "Case #%d: %s" % ( cNum, "NO" if answer else "YES")
 
 
     
 
 
