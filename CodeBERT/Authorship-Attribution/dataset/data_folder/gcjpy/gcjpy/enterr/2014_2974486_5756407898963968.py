#
 # Google Code Jam 2014
 # Roaund 0: A. Magic Trick
 # submission by EnTerr
 #
 
 '''
 ---Input 
 3
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
 
 ---Output 
 Case #1: 7
 Case #2: Bad magician!
 Case #3: Volunteer cheated!
 '''
 
 
 
 import sys
 from time import clock
 
 
 f = open(sys.argv[1])
 def input(): return f.readline().strip();
 
        
 
 #clk = clock()
 
 for caseNo in xrange(1, int(input())+1):
     #first time
     row_no = int(input())
     for i in 1,2,3,4:
         row = input()
         if i == row_no:
             nums = set(row.split())
             
     #second time
     row_no = int(input())
     for i in 1,2,3,4:
         row = input()
         if i == row_no:
             nums &= set(row.split())
 
 #    print >>sys.stderr, caseNo
     if not nums:
         res = 'Volunteer cheated!'
     elif len(nums) > 1:
         res = 'Bad magician!'        
     else:
         res = nums.pop()
     print 'Case #%d:' % caseNo, res
     
 #print >>sys.stderr, 'time= %.1f seconds' % (clock()-clk )
 
