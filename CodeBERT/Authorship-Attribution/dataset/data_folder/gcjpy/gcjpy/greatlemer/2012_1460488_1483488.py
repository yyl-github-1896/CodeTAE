from optparse import OptionParser
 import math
 
 # The largest number B can be
 MAX_NUMBER = 2000000
 
 # COUNT_MAP will store the number of recycled pairs that can exist for a
 # list of cycles of length n (these are the triangular numbers).
 # Calculate this now so that we don't waste time with it later on.
 COUNT_MAP = { 1: 0 }
 index = 1
 while index < math.log10(MAX_NUMBER):
     index += 1
     COUNT_MAP[index] = index * (index - 1) / 2
 
 def solve(minimum, maximum):
     # Store the result
     total_cycles = 0
     # The numbers we need to check.  We'll remove numbers from this once we've
     # used them in a cycle so that we don't attempt to reprocess them.
     iter_range = range(minimum, maximum + 1)
     # Keep looping untli we've gone through all the numbers.
     while iter_range:
         # Remove the first number
         number = iter_range[0]
         iter_range.remove(number)
         # Add this to the list of numbers in a potential cycle.
         cycle_numbers = [number,]
         # Using strings for this feels icky but the modulo arithmetic seems
         # equally icky :-(
         # Double up the number in a string and we'll use slices to get the
         # cycles.
         string_rep = "%s%s" % (number, number)
         digits = len(string_rep) / 2
         start_index, end_index = 0, digits
         while start_index < digits:
             start_index += 1
             end_index += 1
             new_number = int(string_rep[start_index:end_index])
             if new_number == number:
                 # If we're repeating then there's no need to take more slices
                 start_index = digits
             elif new_number > number and new_number <= maximum:
                 # We should already have dealt with numbers lower than this,
                 # and we don't want anything above the maximum. Anything else
                 # add to the cycle options and remove from the list of numbers
                 # to check.
                 cycle_numbers.append(new_number)
                 iter_range.remove(new_number)
         total_cycles += COUNT_MAP[len(cycle_numbers)]
     return total_cycles
 
 def parse_case(data_line):
     bits = data_line.split()
     minimum = int(bits[0])
     maximum = int(bits[1])
     return (minimum, maximum, )
 
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
     	print "Case #%d: %s" % (case_number, solve(*data_args))
 
 if __name__ == "__main__":
     main()