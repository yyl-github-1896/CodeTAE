# coding: utf-8
 import sys
 from itertools import groupby
 
 def testcases():
     with open(sys.argv[1], "r") as f:
         T = int(f.readline())
         for X in range(1, T + 1):
             BOARD = [
                 f.readline().strip(),
                 f.readline().strip(),
                 f.readline().strip(),
                 f.readline().strip(),
             ]
             f.readline()
             yield X, BOARD
 
 def main():
     for X, BOARD in testcases():
         points = [0] * 10
         for iR, cols in enumerate(BOARD):
             cols = list( p(c) for c in cols )
 
             # 
             points[iR] = sum(cols)
 
             # c
             for iC, c in enumerate(cols):
                 points[4 + iC] += c  # c
 
             # ΂
             points[8] += cols[0 + iR]
             points[9] += cols[3 - iR]
 
         status = "Draw"
         for pp in points:
             if pp >= 1000:
                 status = "Game has not completed"
             elif pp in (4, 103):
                 status = "X won"
                 break
             elif pp in (40, 130):
                 status = "O won"
                 break
 
         print("Case #{}: {}".format(X, status))
 
 
 def p(c):
     if  c == 'X':
         return 1
     elif c == 'O':
         return 10
     elif c == 'T':
         return 100
     else:
         return 1000
 
 if __name__=="__main__":
     main()
