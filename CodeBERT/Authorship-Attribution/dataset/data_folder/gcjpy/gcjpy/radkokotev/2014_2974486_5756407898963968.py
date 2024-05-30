filename = raw_input("Name of file: ")
 f = open(filename, "r")
 o = open(filename + ".out", "w")
 
 
 T = int(f.readline()[:-1])
 ## Code starts here
 
 many_possible = "Bad magician!"
 zero_possible = "Volunteer cheated!"
 
 for t in range(1, T + 1):
     first = int(f.readline()[:-1]) - 1
     grid1 = []
     for i in range(4):
         grid1 += [f.readline()[:-1].split(" ")]
         
     second = int(f.readline()[:-1]) - 1
     grid2 = []
     for i in range(4):
         grid2 += [f.readline()[:-1].split(" ")]
 
     possible = []
     for num in grid1[first]:
         if num in grid2[second]:
             possible += [num]
 
     if len(possible) == 1:
         o.write("Case #%d: %s\n" %(t, possible[0]))
     elif len(possible) == 0:
         o.write("Case #%d: %s\n" %(t, zero_possible))
     else:
         o.write("Case #%d: %s\n" %(t, many_possible))
         
     
 ## code ends here
 
 o.close()
 f.close()
