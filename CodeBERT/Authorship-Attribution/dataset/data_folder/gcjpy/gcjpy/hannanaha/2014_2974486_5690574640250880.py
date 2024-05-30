import os
 import time
 import decimal
 import functools
 
 #===============================================================================
 # Generic helpers
 #===============================================================================
 # TODO FOR 14 : rounding functions, graph manipulation, desert lion, AttrDict
 
 #EOL = os.linesep - using this causes weird \r\r\n problems
 EOL = "\n"
 
 # ------------------------------------------------------------------------------
 
 def is_equal_approx(x, y, epsilon=1e-6):
     """Returns True iff y is within relative or absolute 'epsilon' of x.
     
     By default, 'epsilon' is 1e-6.
     """
     # Check absolute precision.
     if -epsilon <= x - y <= epsilon:
         return True
 
     # Is x or y too close to zero?
     if -epsilon <= x <= epsilon or -epsilon <= y <= epsilon:
         return False
 
     # Check relative precision.
     return (-epsilon <= (x - y) / x <= epsilon
         or -epsilon <= (x - y) / y <= epsilon)
   
 def read_syms(fd):
     """Read a line of whitespace separated symbols."""
     return fd.readline().strip().split()
 
 def read_ints(fd):
     """Read a line of whitespace separated integers."""
     return [int(p) for p in read_syms(fd)]
 
 def read_floats(fd):
     """Read a line of whitespace separated floats."""
     return [float(p) for p in read_syms(fd)]
 
 # ------------------------------------------------------------------------------
 
 class Mtrx(object):
     """A matrix object."""
     
     def __init__(self, rows, cols, data):
         assert len(data) == rows * cols
         self.rows = rows
         self.cols = cols
         self.data = data
         
     def cell(self, r, c):
         return self.data[r * self.cols + c]
     
     def getrow(self, i):
         return [self.cell(i, c) for c in xrange(self.cols)]
 
     def getcol(self, i):
         return [self.cell(c, i) for c in xrange(self.rows)]
     
     @classmethod
     def readfromfile(cls, fd, readfunc, rows=None, cols=None):
         """Read matrix from file, assuming first line at location is `R C`.
         
         Return a new Mtrx object. Reading values is performed by the `readfunc`.
         Pre-determined size can be passed using `rows` and `cols`.
         """
         data = []
         if rows is None:
             assert cols is None
             rows, cols = read_ints(fd)
         else:
             assert cols is not None
         for _ in range(rows):
             line = readfunc(fd)
             assert len(line) == cols
             data.extend(line)
         return Mtrx(rows, cols, data)
             
     @classmethod
     def read_int_matrix(cls, fd, rows=None, cols=None):
         return cls.readfromfile(fd, read_ints, rows, cols)
             
     @classmethod
     def read_sym_matrix(cls, fd, rows=None, cols=None):
         return cls.readfromfile(fd, read_syms, rows, cols)
             
     def __str__(self):
         res = ""
         for i in xrange(self.rows):
             res += str(self.getrow(i)) + EOL
         return res
     
     def __repr__(self):
         return "{}({}, {}, {})".format(self.__class__.__name__, self.rows,
                                        self.cols, self.data)
 
 # ------------------------------------------------------------------------------
 
 cachetotals = 0
 cachemisses = 0
 
 def statreset():
     global cachemisses, cachetotals
     cachemisses = 0
     cachetotals = 0
 
 class memoizeit(object):
     """Decorator. Caches a function's return value each time it is called.
     
     If called later with the same arguments, the cached value is returned 
     (not reevaluated).
     """
     
     def __init__(self, func):
         self.func = func
         self.cache = {}
         
     def __call__(self, *args):
         
         # update stats
         global cachetotals, cachemisses
         cachetotals += 1
         
         try:
             return self.cache[args]
         except KeyError:
             
             # update stats
             cachemisses += 1
             
             value = self.func(*args)
             self.cache[args] = value
             return value
         except TypeError:
 
             # update stats
             cachemisses += 1
 
             # uncachable -- for instance, passing a list as an argument.
             # Better to not cache than to blow up entirely.
             return self.func(*args)
     
     @property
     def __name__(self):
         return self.func.__name__
     
     def __get__(self, obj, objtype):
         """Support instance methods."""
         return functools.partial(self.__call__, obj)
 
 # ------------------------------------------------------------------------------
 
 class timeit(object):
     """Decorator that times a function.
     
     When function ends, print name, runtime, return value and cache stats.
     """
     
     def __init__(self, func):
         self.func = func
         
     def __call__(self, *args):
         start = time.time()
         value = self.func(*args)
         delta = time.time() - start
         cachedata = (1 - cachemisses/(cachetotals * 1.0)) if \
             cachetotals else 0
         print self.func.__name__, "{:7.3f}s, (res: {}, cache: {:.2%})".format(
             delta, value, cachedata)
         return value
     
     def __get__(self, obj, objtype):
         return functools.partial(self.__call__, obj)
 
 #===============================================================================
 # Input/output
 #===============================================================================
 
 def read_input(filename):
     data = []
     with open(filename, "r") as f:
         cases = read_ints(f)[0]
         # =============================================
         for _ in xrange(cases):
             case = {}
             case["R"], case["C"], case["M"] = read_ints(f)
             data.append(case)
         # =============================================
     return data
 
 def make_output(fname, output):
     CASE_PRFX = "Case #%s: "
     fname = fname + time.strftime("%H%M%S") + ".out"
     with open(fname, "w") as f:
         restext = []
         print "Output content ==============="
         # =============================================
         for i, outdata in enumerate(output):
             line = CASE_PRFX % (i + 1,) + EOL + str(outdata) + EOL
             print line,
             restext.append(line)
         # =============================================
         print "=" * 30
         f.writelines(restext)
 
 #===============================================================================
 # Actual solution
 #===============================================================================
 
 MINE = "*"
 CLICK = "c"
 UNK = "."
 
 class Board(object):
     
     def __init__(self, r, c):
         self.rows = r
         self.cols = c
         self.edge_row_idx = self.rows - 1
         self.edge_col_idx = self.cols - 1
         self.board = [[UNK for _ in xrange(c)] for _ in xrange(r)]
         self.board[0][0] = CLICK
 
     def fill_edge_row(self, m):
         i = self.edge_col_idx
         while m > 0 and i >= 0:
             self.board[self.edge_row_idx][i] = MINE
             i -= 1
             m -= 1
         self.edge_row_idx -= 1
 
     def fill_edge_col(self, m):
         i = self.edge_row_idx
         while m > 0 and i >= 0:
             self.board[i][self.edge_col_idx] = MINE
             i -= 1
             m -= 1
         self.edge_col_idx -= 1
 
     def __str__(self):
         return EOL.join(["".join(r) for r in self.board])
 
 @memoizeit
 def is_stage_solvable(rows, cols, mines):
     """Return True iff stage is solvable. 
     Also return fill instruction:
     0 if impossible/dontcare, 1 to fill row, 2 to fill column, 
     3 for row special (most in the row), 4 for col special (most in the col)
     """
     rc = rows * cols
     
     # all full
     if mines == rc:
         return False, 0
 
     if rows == 1:
         return mines <= rc - 1, 2
     if cols == 1:
         return mines <= rc - 1, 1
     
     # rows and cols > 1
     # single cell in corner   
     if mines == rc - 1:
         return True, 1  # doesn't matter what to fill
     
     # won't find 4 cells for the corner
     if mines > rc - 4:
         return False, 0
     
     if rows == 2:
         return (False, 0) if mines == 1 else (True, 2)
     if cols == 2:
         return (False, 0) if mines == 1 else (True, 1)
         
     # rows and cols > 2
     if rows <= cols:
         # try to fill columns
         if mines >= rows:
             return True, 2
         if mines == rows - 1:
             if mines == cols - 1:
                 if rows == 3:
                     return False, 0
                 return True, 4 # L shape fill, most in the column
             else:
                 return True, 1 # fill row
         return True, 2 
     else:
         # try to fill rows
         if mines >= cols:
             return True, 1
         if mines == cols - 1:
             if mines == rows - 1:
                 if cols == 3:
                     return False, 0
                 return True, 3 # L shape fill, most in the row
             else:
                 return True, 2 # fill column
         return True, 1 
 
 @timeit
 def solveit(case):
     rows = case["R"]
     cols = case["C"]
     mines = case["M"]
     
     b = Board(rows, cols)
     r, c, m = rows, cols, mines
     
     while m >= 0:
         okgo, howtofill = is_stage_solvable(r, c, m)
         if not okgo:
             return "Impossible"
         if howtofill == 1: # fill row
             b.fill_edge_row(m)
             if m <= c:
                 break # fill and done
             m -= c
             r -= 1
         elif howtofill == 2: # fill column
             b.fill_edge_col(m)
             if m <= r:
                 break # fill and done
             m -= r
             c -= 1
         elif howtofill == 3: # L shape fill, most in the row
             b.fill_edge_row(m - 1)
             b.fill_edge_col(1)
             break # fill and done
         elif howtofill == 4: # L shape fill, most in the column
             b.fill_edge_col(m - 1)
             b.fill_edge_row(1)
             break # fill and done
         else:
             assert False
 
     return str(b) 
 
 
 #===============================================================================
 # Main
 #===============================================================================
 
 @timeit
 def main(fname):
     data = read_input(fname)
     output = []
     for case in data:
         statreset() # reset cache stats
         # =============================================
         res = solveit(case)
         output.append(res)
         # =============================================
     make_output(fname, output)
 
 
 if __name__ == '__main__':
 #    main("sample.in")
     main("C-small-attempt0.in")
 #    main("B-large.in")
 #    main("B-small-attempt0.in")
 #    main("A-large.in")