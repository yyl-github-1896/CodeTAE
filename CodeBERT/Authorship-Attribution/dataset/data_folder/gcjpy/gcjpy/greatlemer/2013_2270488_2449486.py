from optparse import OptionParser
 import string
 
 def solve(rows,cols,width,height):
     # Calculate the lowest setting that can be used when cutting a row or col.
     row_mins = [max(row) for row in rows]
     col_mins = [max(col) for col in cols]
     for row_idx in range(height):
         for col_idx in range(width):
             if row_mins[row_idx] > rows[row_idx][col_idx] \
                and col_mins[col_idx] > rows[row_idx][col_idx]:
                 return "NO"
     return "YES"
 
 
 def parse_case(data,width,height):
     data_line = [int(entry) for entry in reduce(lambda x,y: x+y, data, [])]
     rows = []
     cols = []
     for idx in range(height):
         offset = idx * width
         # Pull rows
         rows.append(data_line[offset:offset+width])
     for idx in range(width):
         # Pull columns
         cols.append(data_line[idx::width][:height])
     return (rows, cols, width, height)
 
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
         height,width = input_file.readline().split()
         width = int(width)
         height = int(height)
         data = []
         for idx in range(height):
             data.append(input_file.readline().split())
         data_args = parse_case(data, width, height)
         print "Case #%d: %s" % (case_number, solve(*data_args))
 
 if __name__ == "__main__":
     main()