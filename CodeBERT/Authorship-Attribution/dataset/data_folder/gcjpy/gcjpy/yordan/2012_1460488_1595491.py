#!/usr/bin/env python
 
 
 def best(total):
     """Return the best possible score for the given `total`.  Assume
     the total is computed by summing exactly three scores (each in the
     interval of 0 to 10 inclusive) and no score can be 2 points apart
     from another.
     
     Arguments:
     - `total`:
     """
     m = total % 3
     if m == 2:
         b = total // 3 + 2
     else:
         b = total // 3 + 1
     if b > 10:
         b = 10
     return b
 
 def best_non_surprising(total):
     """Return the best possible score for the given `total`, but
     assume that there should be no more than 1 point difference
     between the scores.
 
     Arguments:
     - `total`:
     """
     if total % 3 == 0:
         return total // 3
     else:
         return total // 3 + 1
 
 def max_num_gte_p(totals, S, p):
     """Return the maximum number of Googlers that could have had a
     best result of at least p.
     
     Arguments:
     - `totals`:
     - `S`: number of surprising triplets of scores
     - `p`:
     """
     res = 0
     for total in totals:
         if total == 0:
             if p == 0:
                 res += 1
             continue
 
         if best_non_surprising(total) >= p:
             # print total, 'non_surp --> ', best_non_surprising(total)
             res += 1
         elif S > 0 and best(total) >= p:
             # print total, 'surp --> ', best(total)
             res += 1
             S -= 1
 
     return res
 
 def main():
     import sys
     with open(sys.argv[1], 'r') as f:
         f.readline()            # skip T
 
         n = 0
         for line in f:
             n += 1
 
             line = [int(s) for s in line.split()]
             N = line[0]
             S = line[1]
             p = line[2]
             totals = line[3:]
 
             # print 'S=%d, p=%d, Totals: ' % (S, p), totals
             print 'Case #%d: %d' % (n, max_num_gte_p(totals, S, p))
             # print
 
 if __name__ == '__main__':
     main()
