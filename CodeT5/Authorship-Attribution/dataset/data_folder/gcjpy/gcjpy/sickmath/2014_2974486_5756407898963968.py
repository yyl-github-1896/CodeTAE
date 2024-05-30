f = open('input.in')
 g = open('output', 'w')
 
 T = int(f.readline()[:-1])
 
 for case in xrange(T) :
     a1 = int(f.readline()[:-1])
     M1 = [map(int, f.readline()[:-1].split()) for i in range(4)]
     a2 = int(f.readline()[:-1])
     M2 = [map(int, f.readline()[:-1].split()) for i in range(4)]
     r1 = M1[a1-1]
     r2 = M2[a2-1]
     res = set(r1).intersection(set(r2))
     if len(res) == 1 : res = res.pop()
     elif len(res) == 0 : res = 'Volunteer cheated!'
     else : res = 'Bad magician!'
     output = 'Case #' + str(case + 1) + ': ' + str(res)
     g.write(output + '\n')
     print output
 
 f.close()
 g.close()
