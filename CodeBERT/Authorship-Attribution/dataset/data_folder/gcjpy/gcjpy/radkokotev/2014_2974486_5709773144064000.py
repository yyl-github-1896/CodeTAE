filename = raw_input("Name of file: ")
 infile = open(filename, "r")
 outfile = open(filename + ".out", "w")
 
 
 T = int(infile.readline()[:-1])
 ## Code starts here
 
 
 def getMinTime(c, f, x):
     p0 = 2.0
     s_prev = x / p0
     s_curr = c / p0
     prev_item = 0
     next_item = x / (p0 + f)
     n = 1
     while s_prev + prev_item > s_curr + next_item:
         s_prev = s_curr
         prev_item = next_item
         s_curr += c / (p0 + (n * f))
         next_item = x / (p0 + ((n + 1) * f))
         n += 1
     return s_prev + prev_item
 
 for t in range(1, T + 1):
     items = infile.readline()[:-1].split(" ")
     c = float(items[0])
     f = float(items[1])
     x = float(items[2])
     time = getMinTime(c, f, x)
     outfile.write("Case #%d: %.7f\n" %(t, time))
     
         
     
 ## code ends here
 
 outfile.close()
 infile.close()
