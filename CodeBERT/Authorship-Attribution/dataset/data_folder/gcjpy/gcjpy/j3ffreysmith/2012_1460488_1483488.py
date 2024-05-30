#!/usr/bin/env python
 
 def partCa(infile="C:/Users/Jeffrey/Dropbox/Google Code Jam/2011/Qualifiers/C/C-small-attempt0.in",\
               outfile="C:/Users/Jeffrey/Dropbox/Google Code Jam/2011/Qualifiers/C/output.txt"):
     
     #if not init:
         #build_dict()
     
     #Reading input
     linesA = []
     for line in open(infile, 'r'):
         linesA.append(line.strip())
 
     outA = []
         
     #Parsing Input
     T = int(linesA[0])
     for i in range(1, 1 + T):
         caseA = linesA[i].split()
         A = int(caseA[0])
         B = int(caseA[1])
         
         
         outA.append(0)
         #Calculating answer
         for i in range(A,B):
             for j in range(i + 1, B + 1):
                 #testing pair (i, j)
                 outA[-1] += int(isRecycled(i, j))
     
     #Writing Output
     out = open(outfile, 'w')
     print "\nOUTPUT"
     for i in range(1, 1 + T):
         if i != 1:
             out.write("\n")
         print "Case #" + str(i) + ": " +str(outA[i-1])
         out.write("Case #" + str(i) + ": " +str(outA[i-1]))
     out.close()
     
 def isRecycled(n,m):
     '''
     Takes 2 integers and tells you if they are recycled
     '''
     a = str(n)
     b = str(m)
     if len(a) == len(b):
         for i in range(len(a)):
             if (a[i:] + a[:i]) == b:
                 return True
         
     return False
     
 if __name__ == "__main__":
     partCa()
