#Template code developed by Brett Olsen (brett.olsen@gmail.com), 2013
 #for the Google Code Jam programming contest
 
 ###############################################################################
 # Imports go here
 ###############################################################################
 
 from __future__ import division
 import numpy as np
 
 ###############################################################################
 # Global variables (for caching, etc.) go here
 ###############################################################################
 
 #Set up the input/output files: problem-tagsuffix.in / *.out
 problem = "B"
 tag = "small" #commonly sample, small, or large
 #tag = "large"
 #tag = "sample"
 suffix = "-attempt0" #used sometimes for indexing later input files
 #suffix = ""
 
 ###############################################################################
 # Helper functions go here
 ###############################################################################
 
 
 def read_input(infile):
     """This function should take an open input file, load in all of the
     relevant information for a single case of the problem, and output it
     as a single object.    
     """
     #Some utility functions to read in particular types of input
     def read_int():
         return int(infile.readline().strip())
     def read_ints():
         return np.array(infile.readline().split(), dtype=int)
     def read_float():
         return float(infile.readline().strip())
     def read_floats():
         return np.array(infile.readline().split(), dtype=float)
     def read_string():
         return infile.readline().strip()
     def read_strings():
         return np.array(infile.readline().split(), dtype=object) #change the dtype?
     
     N, M = read_ints()
     
     lawn = np.empty((N, M), dtype=int)
     for i in range(N):
         row = read_ints()
         assert len(row) == M
         lawn[i,:] = row
     
     return lawn
 
 def solve_case(case):
     """Take the input data (structured in case) and perform any necessary
     calculations to obtain the desired output, formatted as the appropriate
     string.    
     """
     
     lawn = case
     undefined = np.zeros(lawn.shape, dtype=bool)
     
     colvals, rowvals = np.meshgrid(range(lawn.shape[1]), range(lawn.shape[0]))
     
     while not undefined.all():
         #Find the lowest still-defined point in the lawn
         valid = undefined == False
         minval = lawn[valid].min()
     
         minindex = np.where(lawn[valid] == minval)[0][0]
         minrow = rowvals[valid][minindex]
         mincol = colvals[valid][minindex]
         #Check to see if this point's row could have been mowed
         if (lawn[minrow,:][valid[minrow,:]] == minval).all():
             #Undefine this row
             undefined[minrow,:] = True
             continue
         
         #Otherwise, check to see if this point's column could have been mowed
         if (lawn[:,mincol][valid[:,mincol]] == minval).all():
             #Undefine this column
             undefined[:,mincol] = True
             continue
         
         #Otherwise, it's invalid!
         return "NO"
     
     return "YES"
 
 ###############################################################################
 # Main execution path
 ###############################################################################
 
 if __name__ == "__main__":
     #Open up the input & output files
     infile = open("%s-%s%s.in" % (problem, tag, suffix), 'r')
     outfile = open("%s-%s%s.out" % (problem, tag, suffix), 'w')
     
     #Read in the number of cases (the first input line) to iterate through
     cases = int(infile.readline().strip('\n'))
     for i in range(cases):
         
         #Read in the input data for this case
         case = read_input(infile)
         
         #Solve the problem for this case
         output = solve_case(case)
         
         #Write out the output of this case
         outfile.write('Case #%i: %s\n' % (i+1, output))
         print 'Case #%i: %s\n' % (i+1, output)
     
     #Close files
     infile.close()
     outfile.close()