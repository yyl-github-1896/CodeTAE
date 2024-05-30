# coding:utf-8
 import sys
 
 def testcases():
     with open(sys.argv[1], "r") as f:
         f.readline()  # skip number of testcases
         for X, T in enumerate(f, 1):
             yield X, [int(t) for t in T.split()]
 
 def main():
     for X, T in testcases():
         N = T[0]   # the number of Googlers
         S = T[1]   # the number of surprising triplets of scores
         p = T[2]   # best result of at least
 
         y = 0
 
         for t in T[3:]:
             d, m = divmod(t, 3)
             if m == 0:
                 if p <= d:
                     y += 1
                 elif 0 <= d - 1 <= p <= d + 1 <= 10 and S:
                     y += 1
                     S -= 1
             elif m == 1:
                 if p <= d + 1:
                     y += 1
             else:
                 if p <= d + 1:
                     y += 1
                 elif p <= d + 2 and S:
                     y += 1
                     S -= 1
 
         print("Case #{:d}: {:d}".format(X, y))
 
 if __name__=="__main__":
     main()
