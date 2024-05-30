f = open('A.in', 'r')
 g = open('outputA.txt', 'w')
 data = [[int(e) for e in line.strip("\n").split(' ')] for line in f]
 T = data[0][0]
 c = 0
 for i in xrange(1, T*10 + 1, 10):
     c += 1
     choice1 = data[i][0]
     choice2 = data[i+5][0]
     grid1, grid2 = [], []
     for j in xrange(1,5):
         grid1.append(data[i+j])
 
     for j in xrange(6, 10):
         grid2.append(data[i+j])
 
     s1 = set(grid1[choice1-1])
     s2 = set(grid2[choice2-1])
 
     s = s1 & s2
     if len(s) == 1:
         g.write("Case #%i: %i\n" %(c, s.pop()))
     elif not s:
         g.write("Case #%i: Volunteer cheated!\n" %(c))
     else:
         g.write("Case #%i: Bad magician!\n" %(c))
 
 f.close()
 g.close()
     
