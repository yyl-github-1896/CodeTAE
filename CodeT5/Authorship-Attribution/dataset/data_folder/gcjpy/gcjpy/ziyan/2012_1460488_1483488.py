import sys
 
 def find_recycled_pairs(A, B):
     count = 0
     l = len(str(A))
     for i in range(A, B + 1):
         variants = []
         for d in range(1, l):
             fixed = str(i)[:d]
             moving = str(i)[-(l - d):]
             j = int(moving + fixed)
             if j != i and len(str(i)) == len(str(j)) and j in range(A, B + 1) and j not in variants:
                 variants.append(j)
                 #print '%s -> %s' % (fixed + moving, moving + fixed)
                 count = count + 1
     return count / 2
 
 
 def find_recycled_pairs_efficient(A, B):
     count = 0
     sa = str(A)
     sb = str(B)
     l = len(sa)
     for fixed in range(1, l):
         moving = l - fixed
         x = int(sa[:fixed])
         y = int(sb[:fixed])
         m = int(sa[-fixed:])
         n = int(sb[-fixed:])
         j = int(sa[:moving])
         k = int(sb[:moving])
         print '%i fixed: x = %i, m = %i, n = %i, y = %i, j = %i, k = %i' % (fixed, x, m, n, y, j, k)
 
         if int(str(y) + str(k)) >= B:
             k1 = int(sb[-moving:])
             print 'k1 - j = %i - %i' % (k1, j)
             if k1 > j:
                 count = count + (k1 - j)
         if int(str(x) + str(j)) <= A:
             j1 = int(sa[-moving:])
             print 'k - j1 = %i - %i' % (k, j1)
             if k > j1:
                 count = count + (k - j1)
 
         if len(str(k)) >= len(str(x)):
             count = count + (y - x) * (k - j)
         else:
             count = count + (y - x - 1) * (k - j + 1)
 
         if x < m:
             count = count - (m - x - 1)
         if y > n:
             count = count - (y - n - 1)
 
     return count / 2
 
 def main():
 
     case_count = int(sys.stdin.readline())
 
     for case_index in range(1, case_count + 1):
         (A, B) = sys.stdin.readline().strip().split(' ')
         A = int(A)
         B = int(B)
         assert len(str(A)) == len(str(B))
         print 'Case #%i: %s' % (case_index, find_recycled_pairs(A, B))
 
 if __name__ == '__main__':
     main()