filename = raw_input("Name of file: ")
 infile = open(filename, "r")
 outfile = open(filename + ".out", "w")
 
 
 T = int(infile.readline()[:-1])
 ## Code starts here
 
 def addMinesDiagonally(r, c, m):
     field = []
     for i in range (r):
         row = []
         for j in range(c):
             row += ["."]
         field += [row]
         
     for i in range (r + c):
         ver = min (i, r - 1)
         hor = max (0, 1 + i - r)
         while ver >= 0 and hor <= c - 1 and m > 0:
             if m == 1 and hor == c - 2 and ver == r - 2:
                 ver -= 1
                 hor += 1
             field[ver][hor] = "*"
             ver -= 1
             hor += 1
             m -= 1
         
     return field
 
 def isPossible(field):
     if field[-1][-1] != ".":
         return False
     up = True
     left = True
     diag = True
     if len(field) > 1 and field[-2][-1] != ".":
             up = len(field[-1]) <= 1
     if len(field[-1]) > 1 and field[-1][-2] != ".":
             left = len(field) <= 1
     if len(field) > 1 and len(field[-1]) > 1 and field[-2][-2] != ".":
         diag = False
     return (up and left and diag) or \
            ((not up) and (not left) and (not diag))
     
 
 for t in range(1, T + 1):
     items = infile.readline()[:-1].split(" ")
     r = int(items[0])
     c = int(items[1])
     m = int(items[2])
     field = addMinesDiagonally(r, c, m)
     if isPossible(field):
         field[-1][-1] = "c"
         s = ""
         for line in field:
             for cell in line:
                 s += cell
             s += "\n"
         outfile.write("Case #%d:\n%s\n" %(t, s[:-1]))
     else:
         s = "IMPOSSIBLE!!!!\n"
         for line in field:
             for cell in line:
                 s += cell
             s += "\n"
         outfile.write("Case #%d:\n%s\n" %(t, s[:-1]))
         #outfile.write("Case #%d:\n%s\n" %(t, "Impossible"))
     
         
     
 ## code ends here
 
 outfile.close()
 infile.close()
