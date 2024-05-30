from gcjbase import *
 
 NO = "NO"
 YES = "YES"
 
 
 def read_input(filename):
     data = []
     with open(filename, "r") as f:
         cases = read_ints(f)[0]
         # =============================================
         for _ in xrange(cases):
             field = IntMatrix()
             field.readfromfile(f)
             data.append(field)
         # =============================================
     return data
 
 def make_output(fname, output):
     CASE_PRFX = "Case #%s: "
     fname = fname + time.strftime("%H%M%S") + ".out"
     with open(fname, "w") as f:
         # =============================================
         restext = []
         print "Output content ==============="
         for i, v in enumerate(output):
             line = CASE_PRFX % (i+1,) + str(v) + "\n"
             print line[:-1]
             restext.append(line)
         print "=" * 30
         f.writelines(restext)
         # =============================================
 
 # ----------------------------------------------------------------------
 
 @timeit
 def solveit(case):
     print case
     for row in range(case.rows):
         for col in range(case.cols):
             cell = case.cell(row, col)
             if (any([c > cell for c in case.getrow(row)]) and
                 any([c > cell for c in case.getcol(col)])):
                 return NO
     return YES
         
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
 #    main("sample.in")
     main("small.in")
     #main("large.in")