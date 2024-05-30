import sys
 
 
 lines = [map(int, line.strip().split(" ")) for line in open(sys.argv[1]).readlines()]
 [count] = lines[0]
 assert count * 10 + 1 == len(lines)
 
 for i in xrange(count):
     base = i*10
     [n1] = lines[base+1]
     [n2] = lines[base+6]
     row1 = set(lines[base+1+n1])
     row2 = set(lines[base+6+n2])
     common = row1.intersection(row2)
     print "Case #%s:" % (i+1),
     if len(common) == 1:
         print list(common)[0]
     elif not common:
         print "Volunteer cheated!"
     else:
         print "Bad magician!"
