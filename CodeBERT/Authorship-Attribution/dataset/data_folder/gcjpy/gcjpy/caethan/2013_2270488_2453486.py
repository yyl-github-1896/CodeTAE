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
 problem = "A"
 tag = "small" #commonly sample, small, or large
 suffix = "-attempt1" #used sometimes for indexing later input files
 
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
     
     board = np.empty((4,4), dtype=int)
     
     dic = {'X': 1, 'T': 2, 'O': 3, '.': 4}
     
     #Read in rows
     for i in range(4):
         line = read_string()
         for j in range(4):
             board[i,j] = dic[line[j]]
     infile.readline()
     
     return board
 
 def iswin(row):
     if 4 in row:
         return None #gap
     if (row <= 2).all():
         return "X won"
     if (row >= 2).all():
         return "O won"
     return None
 
 def solve_case(case):
     """Take the input data (structured in case) and perform any necessary
     calculations to obtain the desired output, formatted as the appropriate
     string.    
     """
     
     board = case
 
     #Look for win conditions
     for i in range(4):
         row = board[i,:]
         if iswin(row) is not None:
             return iswin(row)
         
     for i in range(4):
         col = board[:,i]
         if iswin(col) is not None:
             return iswin(col)
         
     vals = np.arange(4)
     diag = board[vals,vals]
     if iswin(diag) is not None:
         return iswin(diag)
     
     diag = board[vals, vals[::-1]]
     if iswin(diag) is not None:
         return iswin(diag)
 
     #Check if the board is completed (has empty squares left)
     if 4 in board:
         return "Game has not completed"
     
     return "Draw"
 
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