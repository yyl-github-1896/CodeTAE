directory = 'C:/users/me/desktop/google code jam/2014/qualification/C/'
 
 from copy import deepcopy
 import itertools
 
 
 def solve_one_case (R,C,M):
         l = []
         for i in range(R):
             for j in range(C):
                 l.append((i,j))
 
         empty_mat = []
         for i in range(R):
             empty_mat.append(['.']*C)
 
         found = False
 
         assert (0,0) in l
         l = l[1:]
         l = l[::-1]
         assert (0,0) not in l
         
         output = ''
         
         for mine_placement in itertools.combinations(l,M):
             mat = deepcopy(empty_mat)
             for cell in mine_placement:
                 mat[cell[0]][cell[1]] = '*'
             if isOneClick(mat, R, C, M):
                 mat[0][0] = 'c'
                 for line in mat:
                     output += ''.join(line) + '\n'
                 found = True
                 return output
             
         if not found:
             return 'Impossible\n'
         
         assert ValueError()
         
 def solve (f_in, f_out):
     T = int(f_in.readline())
     for testcase in range(1,T+1):
         line = f_in.readline()
         R,C,M = [int(q) for q in line.split()]
         print (testcase,R,C,M)
 
         output = solve_one_case (R,C,M)
         f_out.write('Case #' + str(testcase) + ':\n')
         f_out.write(output)
 
         
 
 
 def isOneClick (mat, R, C, M):
 ##    if mat[0][0] != '.':
 ##        return False
 ##    assert len(mat) == R
 ##    lens = [len(l) for l in mat]
 ##    assert min(lens) == C
 ##    assert max(lens) == C
 ##    assert sum([l.count('*') for l in mat]) == M
 
     mat_cpy = deepcopy(mat)
     oneclickcells = [(0,0)]
     while oneclickcells:
         node = oneclickcells.pop()
         mat_cpy[node[0]][node[1]] = 'v'
         if noNearbyMines(mat_cpy,node):
             oneclickcells.extend(getNearbyUnvisited(mat_cpy, node))
 
     #print (mat_cpy)
     return sum([l.count('.') for l in mat_cpy]) == 0
     
 
 def getNearbyUnvisited(mat, node):
     R = len(mat)
     C = len(mat[0])
     deltas_r = [0]
     deltas_c = [0]
     if node[0] > 0:
         deltas_r.append(-1)
     if node[1] > 0:
         deltas_c.append(-1)
     if node[0] < R-1:
         deltas_r.append(1)
     if node[1] < C-1:
         deltas_c.append(1)
 
     ret_list = []
     for delta_r in deltas_r:
         for delta_c in deltas_c:
             next_node = (node[0]+delta_r, node[1] + delta_c)
             if mat[next_node[0]][next_node[1]] not in ['*','v']:
                 ret_list.append((next_node[0],next_node[1]))
 
     return ret_list
 
 def noNearbyMines(mat,node):
     R = len(mat)
     C = len(mat[0])
     deltas_r = [0]
     deltas_c = [0]
     if node[0] > 0:
         deltas_r.append(-1)
     if node[1] > 0:
         deltas_c.append(-1)
     if node[0] < R-1:
         deltas_r.append(1)
     if node[1] < C-1:
         deltas_c.append(1)
 
     for delta_r in deltas_r:
         for delta_c in deltas_c:
             if mat[node[0] + delta_r][node[1] + delta_c] == '*':
                 return False
     return True
     
 def main_run():
     import os
     import time
     filenames = [x for x in os.listdir (directory)]
     filenames = [x for x in filenames if x.endswith('.in')]
     l1 = [(os.stat(directory+x).st_mtime, x) for x in filenames]
     chosen_filename =  sorted(l1)[-1][1][:-3]
 
     print ('Directory : ', directory)
     print ('Chosen Filename : ',chosen_filename)
     print()
     print ('Start : ', time.ctime())
     print()
     
     f_in = open(directory+chosen_filename+'.in')
     f_out = open(directory+chosen_filename+'.out', 'w')
     solve(f_in,f_out)
     f_in.close()
     f_out.close()
 
     print ()
     print ('End : ', time.ctime())
 
 
 main_run()
 
 ##bads = []
 ##goods = []
 ##
 ##for R in range(1,6):
 ##    for C in range(1,6):
 ##        for M in range(1,R*C+1):
 ##            print (R,C,M)
 ##            output = solve_one_case (R,C,M)
 ##            if output[0] == 'I':
 ##                bads.append((R,C,M))
 ##            else:
 ##                goods.append((R,C,M))
 ##
