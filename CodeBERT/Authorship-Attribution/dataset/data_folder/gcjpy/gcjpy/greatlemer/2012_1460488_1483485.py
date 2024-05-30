from optparse import OptionParser
 import string
 
 def solve(data_line):
     english, googlerese = generate_map()
     transmap = string.maketrans(googlerese, english)
     return string.translate(data_line, transmap, "\n")
 
 def parse_case(data_line):
     return (data_line, )
 
 def generate_map():
     """ Use the known phrases we have to generate a translation map.  If
         there's exactly one letter missing after analysing these phrases (which
         there is) we can work it out by seeing what's left over."""
     known_mappings = {"a zoo": "y qee",
                       "our language is impossible to understand": "ejp mysljylc kd kxveddknmc re jsicpdrysi",
                       "there are twenty six factorial possibilities": "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd",
                       "so it is okay if you want to just give up": "de kr kd eoya kw aej tysr re ujdr lkgc jv",
                      }
     all_letters = "abcdefghijklmnopqrstuvwxyz"
     letter_map = {}
     for english, googlerese in known_mappings.items():
         pairs = zip(english, googlerese)
         for e,g in pairs:
             if e not in letter_map:
                 letter_map[e] = g
     if len(letter_map) == 26:
         e_letter = ""
         g_letter = ""
         for letter in all_letters:
             if not e_letter and letter not in letter_map.keys():
                 e_letter = letter
             if not g_letter and letter not in letter_map.values():
                 g_letter = letter
         letter_map[e_letter] = g_letter
     return "".join(letter_map.keys()), "".join(letter_map.values())
 
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