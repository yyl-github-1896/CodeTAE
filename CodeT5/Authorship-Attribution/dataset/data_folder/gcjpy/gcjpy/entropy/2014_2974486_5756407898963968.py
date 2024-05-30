#!/usr/bin/python
 
 filename = "A-small-attempt0.in"
 
 inp = open(filename, "rU")
 
 n = int(inp.readline().strip())
 
 for case in range(1, n+1):
     gr = lambda x: [list(map(int, inp.readline().strip().split(" "))) for p in range(4)][x-1]
     ans1 = int(inp.readline().strip())
     row1 = set(gr(ans1))
     ans2 = int(inp.readline().strip())
     row2 = set(gr(ans2))
     sect = row1 & row2
     if len(sect) <= 0:
         print("Case #{}: Volunteer cheated!".format(case))
     elif len(sect) == 1:
         print("Case #{}: {}".format(case, sect.pop()))
     elif len(sect) > 1:
         print("Case #{}: Bad magician!".format(case))
     else:
         print("ERROR")
