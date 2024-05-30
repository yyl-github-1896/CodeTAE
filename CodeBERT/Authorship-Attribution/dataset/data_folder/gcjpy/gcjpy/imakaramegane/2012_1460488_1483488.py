import sys
 
 def testcases():
     with open(sys.argv[1], "r") as f:
         f.readline()  # skip number of testcases
         for X, T in enumerate(f, 1):
             yield X, [int(t) for t in T.split()]
 
 def main():
     for X, T in testcases():
         A = T[0]
         B = T[1]
         y = 0
         strA = str(A)
         for n in range(B, A - 1, - 1):
             b = str(n)
             chk = set()
             for i in range(1, len(b)):
                 a = b[i:] + b[:i]
                 if a not in chk and strA <= a < b:
                     chk.add(a)
                     y += 1
 
         print("Case #{:d}: {:d}".format(X, y))
 
 if __name__=="__main__":
     main()
