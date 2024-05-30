# Written for Python 2.7.5
 
 from optparse import OptionParser
 from StringIO import StringIO
 import sys
 
 # Expected format of TEST_CASES is a list of tuples of (input, expected_output)
 TEST_CASES = [
     ("""3
 2
 1 2 3 4
 5 6 7 8
 9 10 11 12
 13 14 15 16
 3
 1 2 5 4
 3 11 6 15
 9 10 7 12
 13 14 8 16
 2
 1 2 3 4
 5 6 7 8
 9 10 11 12
 13 14 15 16
 2
 1 2 3 4
 5 6 7 8
 9 10 11 12
 13 14 15 16
 2
 1 2 3 4
 5 6 7 8
 9 10 11 12
 13 14 15 16
 3
 1 2 3 4
 5 6 7 8
 9 10 11 12
 13 14 15 16
 ""","""Case #1: 7
 Case #2: Bad magician!
 Case #3: Volunteer cheated!
 """),
     ("""1
 1
 15 9 16 5
 6 10 1 3
 2 4 12 11
 13 14 8 7
 1
 5 10 9 6
 12 15 1 11
 14 16 4 2
 13 3 8 7""","""Case #1: Bad magician!
 """)
 ]
 
 BAD_MAGIC = "Bad magician!"
 CHEATING = "Volunteer cheated!"
 
 def parse_input(input_reader):
     case_count = int(input_reader.readline())
     case_idx = 0
     while case_count > case_idx:
         case_idx += 1
         rows = []
         for loop_idx in (1,2):
             row_idx = int(input_reader.readline())
             for idx in (1,2,3,4):
                 if idx == row_idx:
                     rows.append(set(input_reader.readline().rstrip("\n").split(" ")))
                 else:
                     input_reader.readline()
         input_values = {"rows":rows,
                         "case":case_idx}
         yield input_values
 
 
 def solve_problem(output_writer=sys.stdout, **kwargs):
     rows = kwargs['rows']
     case = kwargs['case']
     intersect = rows[0].intersection(rows[1])
     if not intersect:
         msg = CHEATING
     elif len(intersect) == 1:
         msg = intersect.pop()
     else:
         msg = BAD_MAGIC
     print >>output_writer, "Case #%d: %s" % (case, msg)
 
 def solve_inputs(input_reader, output_writer):
     """
     Loop through each problem input in input reader and solve it.
 
     Outputs responses to output_writer.
     """
     for input_values in parse_input(input_reader):
         solve_problem(output_writer=output_writer, **input_values)
 
 def run_tests():
     """
     Check the sample input and output match.
     """
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
         input_reader.close()
         output_writer.close()
     if all_pass:
         print "All tests were successful!"
     else:
         print "Something didn't match - try again."
         print problem_output
 
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