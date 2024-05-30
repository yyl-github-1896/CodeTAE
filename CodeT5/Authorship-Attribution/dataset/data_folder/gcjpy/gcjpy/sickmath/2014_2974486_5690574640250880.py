f = open('input.in')
 g = open('output', 'w')
 
 T = int(f.readline()[:-1])
 
 for case in xrange(T) :
     R, C, M = map(int, f.readline()[:-1].split())
     FREE = R*C - M
     if FREE == 0 : res = '\nImpossible'
     elif FREE != 1 and M > 0 and (R == 2 or C == 2) and (FREE == 2 or FREE % 2 == 1) : res = '\nImpossible'
     elif R > 2 and C > 2 and FREE in (2, 3, 5, 7) : res = '\nImpossible'
     else :
         MAP = [['.' for c in range(C)] for r in range(R)]
         MAP[0][0] = 'c'
         if R == 1 :
             for i in range(C-1, C-M-1, -1) : MAP[0][i] = '*'
         elif C == 1 :
             for i in range(R-1, R-M-1, -1) : MAP[i][0] = '*'
         elif R == 2 :
             for i in range(C-1, C-M/2-1, -1) : MAP[0][i], MAP[1][i] = '*', '*'
             if FREE == 1 : MAP[1][0] = '*'
         elif C == 2 :
             for i in range(R-1, R-M/2-1, -1) : MAP[i][0], MAP[i][1] = '*', '*'
             if FREE == 1 : MAP[0][1] = '*'
         else :
             com = M / C
             for i in range(R-1, max(R-com-1, 2), -1) :
                 MAP[i] = ['*' for j in range(C)]
                 M -= C
             I = max([i for i, j in enumerate(MAP) if j[0] == '.'])
             if I == 2 :
                 com = M / 3
                 if com == 0 : i = C
                 for i in range(C-1, C-com-1, -1) :
                     MAP[0][i], MAP[1][i], MAP[2][i] = '*', '*', '*'
                     M -= 3
                 if M >= 1 : MAP[2][i-1] = '*'
                 if M >= 2 :
                     if i != 1 : MAP[2][i-2] = '*'
                     else : MAP[1][0] = '*'
             else :
                 for i in range(C-1, C-M-1, -1) : MAP[I][i] = '*'
                 if i == 1 :
                     MAP[I][i] = '.'
                     MAP[I-1][C-1] = '*'
         res = '\n' + '\n'.join([''.join(i) for i in MAP])
     output = 'Case #' + str(case + 1) + ': ' + str(res)
     g.write(output + '\n')
     print output
 
 f.close()
 g.close()
