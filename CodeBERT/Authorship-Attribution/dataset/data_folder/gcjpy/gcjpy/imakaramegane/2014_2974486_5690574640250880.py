# coding: utf-8
 import sys
 import os.path
 import itertools
 from itertools import groupby
 import math
 
 def debug(v):
     pass#print(v)
 
 def read(f):
     t = tuple(int(v) for v in f.readline().split())
     debug(t)
     return t
 
 def readf(f):
     t = tuple(float(v) for v in f.readline().split())
     debug(t)
     return t
 
 def answer(f, X, ans):
     out = "Case #{}:\n{}".format(X, ans)
     f.write(out)
     f.write("\n")
     print(out)
 
 def answer_cells(f, X, cells):
     out = "Case #{}:".format(X)
     f.write(out)
     f.write("\n")
     print(out)
     for row in cells:
         out = "".join(row)
         f.write(out)
         f.write("\n")
         print(out)
 
 def main(inf, outf):
     T, = read(inf)
     for casenmbr in range(1, T + 1):
         R, C, M = read(inf)
 
         if M == 0:
             cells = [['.'] * C for i in range(R)]
             cells[0][0] = 'c'
             answer_cells(outf, casenmbr, cells)
             continue
 
         empty = R * C - M
 
         if empty == 1:
             cells = [['*'] * C for i in range(R)]
             cells[0][0] = 'c'
             answer_cells(outf, casenmbr, cells)
             continue
 
         if R == 1 or C == 1:
             cells = [['.'] * C for i in range(R)]
             m = 0
             for r in range(R):
                 for c in range(C):
                     cells[r][c] = '*'
                     m += 1
                     if m == M:
                         break
                 else:
                     continue
                 break
             cells[-1][-1] = 'c'
             answer_cells(outf, casenmbr, cells)
             continue
 
         if empty in (2, 3, 5, 7):
             answer(outf, casenmbr, "Impossible")
             continue
 
         if (R == 2 or C == 2) and empty % 2:
             answer(outf, casenmbr, "Impossible")
             continue
 
         cells = [['*'] * C for i in range(R)]
 
 
         cells[0][0] = 'c'
         empty -= 1
         cc = 1
         rr = 1
         while empty > 0:
             if cc < C:
                 for r in range(rr):
                     if empty == 2 and r == rr - 1:
                         break
                     cells[r][cc] = '.'
                     empty -= 1
                     if empty == 0:
                         break
                 cc += 1
             if rr < R and empty > 0:
                 for c in range(cc):
                     if empty == 2 and c == cc - 1:
                         break
                     cells[rr][c] = '.'
                     empty -= 1
                     if empty == 0:
                         break
                 rr += 1            
 
         # cnt = 0
         # for row in cells:
         #     for v in row:
         #         if v == '*':
         #             cnt += 1
         # if cnt != M:
         #     raise "!"
         answer_cells(outf, casenmbr, cells)
 
 
 if __name__=="__main__":
     infname = sys.argv[1]
     outfname = os.path.splitext(infname)[0] + ".out"
     with open(infname, "r") as inf:
         with open(outfname, "w") as outf:
             main(inf, outf)
