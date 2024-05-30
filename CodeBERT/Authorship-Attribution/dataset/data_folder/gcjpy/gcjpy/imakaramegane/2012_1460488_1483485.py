import sys
 
 def testcases():
     with open(sys.argv[1], "r") as f:
         f.readline()  # skip number of testcases
         for X, T in enumerate(f, 1):
             yield X, T[:-1]
 
 def main():
     for X, T in testcases():
         tbl = str.maketrans("abcdefghijklmnopqrstuvwxyz",
                             "yhesocvxduiglbkrztnwjpfmaq")
         S = T.translate(tbl)
         print("Case #{:d}: {}".format(X, S))
 
 if __name__=="__main__":
   main()
   
