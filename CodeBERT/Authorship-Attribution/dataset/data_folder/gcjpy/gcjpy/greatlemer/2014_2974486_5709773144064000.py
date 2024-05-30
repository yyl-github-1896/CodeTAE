# Written for Python 2.7.5
 
 from optparse import OptionParser
 from StringIO import StringIO
 from math import ceil
 import sys
 
 # Expected format of TEST_CASES is a list of tuples of (input, expected_output)
 TEST_CASES = [
     ("""4
 30.0 1.0 2.0
 30.0 2.0 100.0
 30.50000 3.14159 1999.19990
 500.0 4.0 2000.0
 ""","""Case #1: 1.0000000
 Case #2: 39.1666667
 Case #3: 63.9680013
 Case #4: 526.1904762
 """)
 ]
 
 """
 Z is number of farms held
 tF(Z) is time to build a farm = C / (2+(F*Z))
 tX(Z) is time to win = X / (2+(F*Z))
 No point incresing Z when tX(Z) < (tX(Z+1) + tF(Z)
     == X / (2+(F*Z)) < (X / (2+(F*(Z+1))) + (C / (2+(F*Z)))
     == (X - C) / (2+(F*Z)) < X / (2+(F*(Z+1)))
     == (X - C) * (2+(F*Z)+F) < X * (2+(F*Z))
     == 2X - 2C + XFZ - CFZ + XF - CF < 2X + XFZ
     == XF - CF - 2C < CFZ
     == (XF - CF - 2C) / CF < Z
 """
 
 def parse_input(input_reader):
     case_count = int(input_reader.readline())
     case_idx = 0
     while case_count > case_idx:
         case_idx += 1
         input_line = input_reader.readline().rstrip("\n").split(" ")
         input_values = {"C": float(input_line[0]),
                         "F": float(input_line[1]),
                         "X": float(input_line[2]),
                         "case": case_idx}
         yield input_values
 
 def solve_problem(output_writer=sys.stdout, **kwargs):
     case = kwargs['case']
     C_val = kwargs['C']
     F_val = kwargs['F']
     X_val = kwargs['X']
 
     best_Z = ((X_val * F_val) - (C_val * F_val) - (2 * C_val)) / (C_val * F_val)
     best_Z = int(ceil(best_Z))
     if best_Z < 0:
         best_Z = 0
 
     tX = lambda z: (X_val / (2+(F_val * z)))
     tF = lambda z: (C_val / (2+(F_val * z)))
 
     total_time = reduce(lambda x,y: x + tF(y), range(best_Z), tX(best_Z))
     print >> output_writer, "Case #%d: %.7f" % (case, total_time)
 
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