fin = open('C-small-attempt0.in', 'r')
 fout = open('C-output.txt', 'w')
 
 cases = int(fin.readline()[:-1])
 
 for case in range(cases) :
     A, B = map(int, fin.readline()[:-1].split(' '))
     digits = len(str(A))
     couples = set()
     for n in range(A,B+1) :
         for t in range(1,digits) :
             m = [str(n)[(i+t)%digits] for i in range(digits)]
             m = int(''.join(m))
             if A <= n < m <= B :
                 couples.add(str([n,m]))
     res = len(couples)
     print 'Case #' + str(case+1) + ': ' + str(res)
     fout.write('Case #' + str(case+1) + ': ' + str(res) + '\n')
     
 fin.close()
 fout.close()
