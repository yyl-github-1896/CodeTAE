import sys
 #sys.stdin = open("b_example.in")
 
 n_cases = input()
 
 def to_ints(s):
     return map(int, s.split())
 
 for case in xrange(1, n_cases + 1):
     ydim, xdim = to_ints(raw_input())
     heights = [to_ints(raw_input()) for _ in xrange(ydim)]
 
     ymaxes = [max(row) for row in heights]
     xmaxes = [max(col) for col in zip(*heights)]
 
     #print ymaxes, xmaxes
 
     poss = True
 
     for y in range(ydim):
         for x in range(xdim):
             height = heights[y][x]
             if not (height == xmaxes[x] or height == ymaxes[y]):
                 poss = False
 
 
     print "Case #%d: %s" % (case, 'YES' if poss else 'NO')
