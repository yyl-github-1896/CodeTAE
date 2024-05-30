from optparse import OptionParser
 
 def solve(N,S,p,t):
     # Easy pickings, if p is 0 then all must win.
     if p == 0:
         return N
     outright_wins = 0
     potential_surprises = 0
     win_cutoff = (p * 3) - 3
     surprise_cutoff = win_cutoff - 2
     for score in t:
         if score == 0:
             continue
         elif score > win_cutoff:
             outright_wins += 1
         elif score > surprise_cutoff:
             potential_surprises += 1
     if potential_surprises < S:
         return outright_wins + potential_surprises
     else:
         return outright_wins + S
 
 def parse_case(data_line):
     bits = data_line.split()
     N = int(bits[0])
     S = int(bits[1])
     p = int(bits[2])
     t = [int(x) for x in bits[3:]]
     return N,S,p,t
 
 def main():
     parser = OptionParser()
     parser.add_option("-f", "--file", dest="filename",
                       help="read input from FILE", metavar="FILE")
 
     (options, args) = parser.parse_args()
     if not options.filename:
         parser.error("Must provide a filename.")
     input_file = open(options.filename, "r")
     total_cases = int(input_file.readline())
     case_number = 0
     while case_number < total_cases:
     	case_number += 1
     	data_args = parse_case(input_file.readline())
     	print "Case #%d: %d" % (case_number, solve(*data_args))
 
 if __name__ == "__main__":
 	main()