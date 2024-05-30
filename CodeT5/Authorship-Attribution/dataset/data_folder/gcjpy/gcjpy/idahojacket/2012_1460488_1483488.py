import time
 
 def get_num_recycled( number_s, limit ):
   num_digits = len(number_s)
   num_s = number_s + number_s
   num = int(number_s)
   r_nums = []
   for i in range( 1, num_digits ):
     r_num_s = num_s[i:num_digits+i]
     r_num = int(r_num_s)
     if ( r_num > num and r_num <= limit ):
       r_nums.append( r_num )
 
   return len(set(r_nums))
 
 
 num_cases = input()
 for i in range( 1, num_cases + 1 ):
   start, limit = raw_input().split()
   num_recycled = 0
   #start_t = time.clock()
   for num in range( int(start), int(limit) + 1 ):
      num_recycled += get_num_recycled( str(num), int(limit) )
   #end_t = time.clock()
   #print start_t, end_t, end_t - start_t
   print 'Case #' + str(i) + ': ' + str( num_recycled )
