import sys
 
 f = open(sys.argv[1])
 T = int(f.readline())
 for test in range(T):
     first_row_index = int(f.readline())
     first_row = []
     for ii in range(4):
         if (ii + 1) == first_row_index:
             first_row = f.readline().strip().split()
         else:
             f.readline()
     second_row_index = int(f.readline())
     second_row = []
     for ii in range(4):
         if (ii + 1) == second_row_index:
             second_row = f.readline().strip().split()
         else:
             f.readline()
     combined = [val for val in first_row if val in second_row]
 
     print "Case #%d:" % (test + 1), "Bad magician!" if len(combined) > 1 else "Volunteer cheated!" if len(combined) == 0 else combined[0]
 
 
