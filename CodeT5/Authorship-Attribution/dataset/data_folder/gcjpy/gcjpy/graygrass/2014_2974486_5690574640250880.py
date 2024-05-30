import os
 
 class Solver(object):
     def __init__(self):
         pass
     
     def solve(self, inputs):
         R, C, M = [int(x) for x in inputs[0].split()]
         mp = []
         for r in range(R):
             mp.append(['.']*C)
         mp[0][0] = 'c'
         outputs = []
         if M == 0:
             for row in mp:
                 outputs.append(''.join(row))
             return outputs
         rr, cc, rm = R, C, M
         while rm >= min(rr, cc):
             if rr <= cc:
                 for r in range(rr):
                     mp[r][cc-1] = '*'
                 cc -= 1
                 rm -= rr
             else:
                 for c in range(cc):
                     mp[rr-1][c] = '*'
                 rr -= 1
                 rm -= cc
         
         if rm == 0:
             if (min(rr, cc), max(rr, cc)) == (1, 2) and min(R, C) != 1:
                 return ['Impossible']
         else:
             if min(rr, cc) - rm >= 2:
                 if rr <= cc:
                     for r in range(rr-rm, rr):
                         mp[r][cc-1] = '*'
                 else:
                     for c in range(cc-rm, cc):
                         mp[rr-1][c] = '*'
             else:
                 if min(rr, cc) >= 4:
                     if rr <= cc:
                         for r in range(2, rr):
                             mp[r][cc-1] = '*'
                         mp[rr-1][cc-2] = '*'
                     else:
                         for c in range(2, cc):
                             mp[rr-1][c] = '*'
                         mp[rr-2][cc-1]='*'
                 elif min(rr,cc) == 3:
                     if max(rr, cc) == 3:
                         return ['Impossible']
                     else:
                         if rr <= cc:
                             mp[2][cc-1] = '*'
                             mp[2][cc-2] = '*'
                         else:
                             mp[rr-1][2] = '*'
                             mp[rr-2][2] = '*'
                 else:
                     return ['Impossible']
                     
         for row in mp:
             outputs.append(''.join(row))
         return outputs
         pass
     
     def feed(self, inputs):
         lines = [x.strip() for x in inputs]
         outputs = []
         test_case_n = int(lines[0])
         cur = 1
         for i in range(test_case_n):
             i = i
             case_line_cnt = 1
             case_inputs = lines[cur:cur+case_line_cnt]
             cur += case_line_cnt
             R, C, M = [int(x) for x in case_inputs[0].split()]
             rslt = self.solve(case_inputs)
             if self.verify(rslt, R, C, M):
                 outputs.append(rslt)
             else:
                 raise 'Failed'
         return outputs
     
     def verify(self, outputs, RR, CC, MCNT):
         if 'Impossible' == outputs[0]:
             return True
         rr = len(outputs)
         cc = len(outputs[0])
         if RR != rr or CC != cc:
             return False
         bd = []
         mask = []
         for i in range(rr):
             mask.append([1]*cc)
             bd.append([0]*cc)
             for j in range(cc):
                 if outputs[i][j] == '*':
                     bd[i][j] = 9
                 elif outputs[i][j] == 'c':
                     start = (i, j)
         for r in range(rr):
             for c in range(cc):
                 if bd[r][c] == 9:
                     for i in [r-1,r,r+1]:
                         for j in [c-1,c,c+1]:
                             if 0 <= i < rr and 0 <= j < cc:
                                 if bd[i][j] != 9:
                                     bd[i][j] += 1
 #         for i, row in enumerate(bd):
 #             print i, row
 
         nlist = [start]
         while len(nlist):
             i, j = nlist.pop(0)
             if mask[i][j] != 0:
                 mask[i][j] = 0
                 if bd[i][j] == 9:
                     raise '!!! BOMB'
                 elif bd[i][j] == 0:
                     for ii in [i-1,i,i+1]:
                         for jj in [j-1,j,j+1]:
                             if 0<=ii<rr and 0<=jj<cc:
                                 if ii != i or jj != j:
                                     nlist.append((ii,jj))
         mcnt = 0
         for r in range(rr):
 #             print mask[r]
             for c in range(cc):
                 if mask[r][c] == 1:
                     mcnt += 1
                 if mask[r][c] == 1 and bd[r][c] != 9:
                     return False
                 if mask[r][c] != 1 and bd[r][c] == 9:
                     return False
         return (mcnt == MCNT)
                 
 
 if __name__ == '__main__':
     iname = 'C-small-attempt0.in'
 #     iname = 'foo'
     sample_in = '''
 7
 5 5 23
 3 1 1
 2 2 1
 4 7 3
 10 10 82
 3 4 0
 2 2 3
     '''
     sample_out = '''
 Case #1: 1.0000000
 Case #2: 39.1666667
 Case #3: 63.9680013
 Case #4: 526.1904762
     '''
     if os.path.exists(iname):
         with open(iname) as f:
             inputs = f.readlines()
     else:
         inputs = [x.strip() for x in sample_in.split('\n') if x.strip()]
     solver = Solver()
     outputs = solver.feed(inputs)
     fail_flag = False
     if os.path.exists(iname):
         with open(iname+'.out', 'w') as f:
             for i, v in enumerate(outputs):
                 print >> f, 'Case #%d:'%(i+1)
                 print >> f, '\n'.join(v)
     print '===================================================='
     for i, v in enumerate(outputs):
         print 'Case #%d:'%(i+1)
         print '\n'.join(v)
     print '===================================================='
     print 'done' if not fail_flag else 'fail'
     pass