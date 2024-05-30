# Written for Python 2.7.5
 
 from optparse import OptionParser
 from StringIO import StringIO
 import sys
 
 # Expected format of TEST_CASES is a list of tuples of (input, expected_output)
 TEST_CASES = [
     ("""5
 5 5 23
 3 1 1
 2 2 1
 4 7 3
 10 10 82
 ""","""Case #1:
 Impossible
 Case #2:
 c
 .
 *
 Case #3:
 Impossible
 Case #4:
 c......
 .......
 .......
 ....***
 Case #5:
 c........*
 .........*
 **********
 **********
 **********
 **********
 **********
 **********
 **********
 **********
 """),
     ("""3
 5 4 3
 5 3 8
 5 5 14
 ""","""Case #1:
 c...
 ....
 ....
 ...*
 ..**
 Case #2:
 Impossible
 Case #3:
 c...*
 ....*
 ...**
 *****
 *****
 """)
 ]
 
 IMPOSSIBLE = "Impossible"
 
 """
 S is number of safe squares = (R*C) - M
 If S == 1 then always possible:
     Assume click in top left, all else mines
 Special cases (R or C is small):
 If R == 1 or C == 1 then always possible:
     Assume click in top left and all safe squares in a line
 Else if R == 2 or C == 2 then possible iff S % 2 == 0:
     Assume click in top left and all safe squares are in a 2 * X line
 Else if R == 3 or C == 3 then possible if S % 3 == 0 (Assume click in top left and all safe squares are in a 3 * X line)
    OR if S % 2 == 0 
 """
 
 def parse_input(input_reader):
     case_count = int(input_reader.readline())
     case_idx = 0
     while case_count > case_idx:
         case_idx += 1
         input_line = [int(x) for x in input_reader.readline().split()]
         input_values = {"case": case_idx,
                         "R": input_line[0],
                         "C": input_line[1],
                         "M": input_line[2]}
         yield input_values
 
 
 def solve_problem(output_writer=sys.stdout, **kwargs):
     case = kwargs['case']
     rows = kwargs['R']
     cols = kwargs['C']
     mines = kwargs['M']
     safe_squares = ((rows * cols) - mines)
     print >> output_writer, "Case #%d:" % case
     row_string = "{:*<%ds}" % cols
     impossible = False
     if safe_squares == 1:
         print >> output_writer, row_string.format("c")
         for row in range(1, rows):
             print >> output_writer, row_string.format("")
     elif rows == 1:
         safe_string = "c" + ("." * (safe_squares - 1))
         print >> output_writer, row_string.format(safe_string)
     elif cols == 1:
         for row in range(rows):
             cell = ""
             if row == 0:
                 cell = "c"
             elif row < safe_squares:
                 cell = "."
             print >> output_writer, row_string.format(cell)
     elif safe_squares == 2:
         impossible = True
     elif rows == 2:
         safe_cols, remainder = divmod(safe_squares, 2)
         if remainder == 1:
             impossible = True
         else:
             safe_string = "." * (safe_cols - 1)
             print >> output_writer, row_string.format("c%s" % safe_string)
             print >> output_writer, row_string.format(".%s" % safe_string)
     elif cols == 2:
         safe_rows, remainder = divmod(safe_squares, 2)
         if remainder == 1:
             impossible = True
         else:
             for row in range(rows):
                 cells = ""
                 if row == 0:
                     cells = "c."
                 elif row < safe_rows:
                     cells = ".."
                 print >> output_writer, row_string.format(cells)
     else:
         safe_rows, remainder = divmod(safe_squares, cols)
         if remainder == 1 and cols == 3 and safe_rows == 2:
             impossible = True
         elif safe_rows > 1:
             if remainder == 1 and safe_rows == 2:
                 mid_safe = "." * (cols-2)
                 for row in range(rows):
                     cell_one = "."
                     mid_cells = mid_safe
                     last_cell = "."
                     if row == 0:
                         cell_one = "c"
                     elif safe_rows == 0:
                         cell_one = "."
                         mid_cells = "." * (remainder + 1)
                     elif safe_rows < 0:
                         cell_one = ""
                         mid_cells = ""
                     if safe_rows < 3:
                         last_cell = ""
                     print >> output_writer, row_string.format("%s%s%s" % (cell_one, mid_cells, last_cell))
                     safe_rows -= 1
             elif remainder == 1:
                 mid_safe = "." * (cols-2)
                 for row in range(rows):
                     cell_one = "."
                     mid_cells = mid_safe
                     last_cell = "."
                     if row == 0:
                         cell_one = "c"
                     elif safe_rows == 0:
                         cell_one = "."
                         mid_cells = "." * remainder
                     elif safe_rows < 0:
                         cell_one = ""
                         mid_cells = ""
                     if safe_rows < 2:
                         last_cell = ""
                     print >> output_writer, row_string.format("%s%s%s" % (cell_one, mid_cells, last_cell))
                     safe_rows -= 1
             else:
                 full_safe = "." * cols
                 for row in range(rows):
                     cells = full_safe
                     if row == 0:
                         cells = "c" + ("." * (cols - 1))
                     elif row == safe_rows:
                         cells = "." * remainder
                     elif row > safe_rows:
                         cells = ""
                     print >> output_writer, row_string.format(cells)
         else:
             safe_cols, remainder = divmod(safe_squares, 2)
             if remainder == 1 and safe_cols < 4:
                 impossible = True
             elif remainder == 0:
                 print >> output_writer, row_string.format("c%s" % ("." * (safe_cols - 1)))
                 print >> output_writer, row_string.format("." * safe_cols)
                 for row in range(2, rows):
                     print >> output_writer, row_string.format("")
             else:
                 safe_cols -= 1
                 print >> output_writer, row_string.format("c%s" % ("." * (safe_cols - 1)))
                 print >> output_writer, row_string.format("." * safe_cols)
                 print >> output_writer, row_string.format("...")
                 for row in range(3, rows):
                     print >> output_writer, row_string.format("")
     if impossible:
         print >> output_writer, IMPOSSIBLE
 
 def solve_inputs(input_reader, output_writer):
     """
     Loop through each problem input in input reader and solve it.
 
     Outputs responses to output_writer.
     """
     for input_values in parse_input(input_reader):
         solve_problem(output_writer=output_writer, **input_values)
 
 def run_tests():
     idx = 0
     all_pass = True
     for problem_input, expected_output in TEST_CASES:
         idx += 1
         input_reader = StringIO(problem_input)
         output_writer = StringIO()
         solve_inputs(input_reader, output_writer)
         problem_output = output_writer.getvalue()
         if problem_output == expected_output:
             print "Test %d: Success" % idx
         else:
             all_pass = False
             print "Test %d: Failure" % idx
             print problem_output
         input_reader.close()
         output_writer.close()
     if all_pass:
         print "All tests were successful!"
     else:
         print "Something didn't match - try again."
 
 def main():
     parser = OptionParser()
     parser.add_option("-f", "--file",
                       dest="filename_stem",
                       help="read input from FILE.in and write to FILE.out",
                       metavar="FILE")
 
     (options, args) = parser.parse_args()
     if options.filename_stem:
         print "Running in file mode."
         input_reader = open("%s.in" % options.filename_stem, "r")
         output_writer = open("%s.out" % options.filename_stem, "w")
         solve_inputs(input_reader, output_writer)
     else:
         print "Running in test mode."
         run_tests()
 
 if __name__ == "__main__":
     main()