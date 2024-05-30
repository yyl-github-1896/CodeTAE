from optparse import OptionParser
 import string
 import pickle
 
 def solve(lower, upper, cache):
     counter = 0
     for item in cache:
         if item > upper:
             break
         if item < lower:
             continue
         counter += 1
     return counter
 
 def is_palindrome(test_int):
     str_arg = str(test_int)
     return str_arg == str_arg[::-1]
 
 def generate_cache():
     """ Generates a list of 'fair and square' numbers between 1 and 10^100
 
     By observation of generating the first few of these numbers it became
     obvious that the 'roots' fitted a very specific pattern, they are either
     single digits and 1,2 or 3; multiple digits consisting of only 1s and 0s;
     multiple digits with a 2 at the beginning and end and 1s and 0s in the
     middle or an odd number of digits with a single 2 in the centre and 1s and
     0s elsewhere.
 
     This function therefore only looks at these numbers to build a list of all
     valid results. """
     # Put 9 in to start with as it's the only one that uses a 3.
     cache = [9,]
     counter = 1
     if upper_bound is None:
         upper_bound = pow(2,25)
     while counter < upper_bound:
         binary_part = "{0:b}".format(counter)
         # Look for palindromes beginning with a 1
         half_int = binary_part
         # Check the odd length palindrome
         pal_int = int(half_int + half_int[:-1][::-1])
         pal_square = pal_int * pal_int
         if is_palindrome(pal_square):
             cache.append(pal_square)
         # Check the even length palindrome
         pal_int = int(half_int + half_int[::-1])
         pal_square = pal_int * pal_int
         if is_palindrome(pal_square):
             cache.append(pal_square)
         half_int = "%s%s" % (binary_part, 2)
         # Check the odd length palindrome only when adding a 2
         pal_int = int(half_int + half_int[:-1][::-1])
         pal_square = pal_int * pal_int
         if is_palindrome(pal_square):
             cache.append(pal_square)
         # Look for palindromes beginning with a 2
         half_int = "2%s" % binary_part[1:]
         # Check the odd length palindrome
         pal_int = int(half_int + half_int[:-1][::-1])
         pal_square = pal_int * pal_int
         if is_palindrome(pal_square):
             cache.append(pal_square)
         # Check the even length palindrome
         pal_int = int(half_int + half_int[::-1])
         pal_square = pal_int * pal_int
         if is_palindrome(pal_square):
             cache.append(pal_square)
         counter += 1
     return sorted(cache)
 
 
 def main():
     parser = OptionParser()
     parser.add_option("-f", "--file", dest="filename",
                       help="read input from FILE", metavar="FILE")
     parser.add_option("-c", "--cache", dest="cache_filename",
                       help="read/write cache from/to CACHE_FILE", metavar="CACHE_FILE")
     parser.add_option("-g", "--generate-cache", dest="generate_cache",
                       help="generate the cache file", action="store_true")
     cache = None
     (options, args) = parser.parse_args()
     if options.generate_cache:
         # Generate a cache file before going through answers so that we don't
         # waste precious time later.
         cache = generate_cache()
         if not options.cache_filename:
             output_file = open(options.cache_filename, "w")
             pickle.dump(cache, output_file)
             output_file.close()
     else:
         cache_file = open(options.cache_filename, "r")
         cache = pickle.load(cache_file)
         cache_file.close()
     if not options.filename:
         parser.error("Must provide a filename.")
     input_file = open(options.filename, "r")
     total_cases = int(input_file.readline())
     case_number = 0
     while case_number < total_cases:
         case_number += 1
         lower,upper = input_file.readline().split()
         lower = int(lower)
         upper = int(upper)
         data_args = (lower, upper, cache)
         print "Case #%d: %s" % (case_number, solve(*data_args))
 
 if __name__ == "__main__":
     main()