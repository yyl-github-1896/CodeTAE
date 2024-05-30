from gcjbase import *
 
 XWON = "X won"
 OWON = "O won"
 DRAW = "Draw" 
 NOTOVER = "Game has not completed"
 
 
 def read_input(filename):
     data = []
     with open(filename, "r") as f:
         cases = read_ints(f)[0]
         # =============================================
         for _ in xrange(cases):
             board = []
             for _ in xrange(4):
                 board.extend(read_syms(f))
             read_syms(f)
             data.append(board)
         # =============================================
     return data
 
 def make_output(fname, output):
     CASE_PRFX = "Case #%s: "
     fname = fname + time.strftime("%H%M%S") + ".out"
     with open(fname, "w") as f:
         # =============================================
         restext = []
         for i, v in enumerate(output):
             line = CASE_PRFX % (i+1,) + str(v) + "\n"
             print line
             restext.append(line)
         f.writelines(restext)
         # =============================================
 
 # ----------------------------------------------------------------------
 
 def getrow(board, i):
     return board[i*4:4*i+4]
 
 def getcol(board, i):
     return [c for j, c in enumerate(board) if j % 4 == i ]
 
 def getdiag(board, i):
     if i == 0:
         return board[0], board[5], board[10], board[15]
     return board[3], board[6], board[9], board[12]
 
 @timeit
 def solveit(case):
     print case
     xcase = [(c if c != 'T' else 'X') for c in case]
     ocase = [(c if c != 'T' else 'O') for c in case]
     
     # rows
     for i in range(4):
         if all([x == 'X' for x in getrow(xcase, i)]):
             return XWON
         if all([x == 'O' for x in getrow(ocase, i)]):
             return OWON
         
     # cols
     for i in range(4):
         if all([x == 'X' for x in getcol(xcase, i)]):
             return XWON
         if all([x == 'O' for x in getcol(ocase, i)]):
             return OWON
         
     # diag
     for i in range(2):
         if all([x == 'X' for x in getdiag(xcase, i)]):
             return XWON
         if all([x == 'O' for x in getdiag(ocase, i)]):
             return OWON
         
     if any([x == '.' for x in case]):
         return NOTOVER
     return DRAW
         
 @timeit
 def main(fname):
     data = read_input(fname)
     output = []
     for i, case in enumerate(data):
         # =============================================
         res = solveit(case)
         output.append(res)
         # =============================================
     make_output(fname, output)
 
 
 if __name__ == '__main__':
     #main("sample.in")
     main("small.in")
     #main("sample.in")