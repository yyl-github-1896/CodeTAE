import sys
 import numpy as np
 
 def isPalindrome(x):
     x = str(x)
     if x[0] != x[-1]:
         return 0
     y = x[::-1]
     if x == y:
         return 1
     return 0
 
 def generate():
     digits = [str(x) for x in range(0,10)]
     dplus = digits + [""]
 
     for x in range(1,10):
         y = x**2
         if isPalindrome(y):
             print y
 
     for x in range(1,10**4):
         x = str(x)
         y = x[::-1]
         pals = [ int(x+z+y)**2 for z in dplus ]
         for p in pals:
             if isPalindrome(p):
                 print p
 
 if __name__ == "__main__":
     #generate()
     #break
     f = open( sys.argv[1] )
     sqpals = np.array([int(l) for l in f])
     sqpals.sort()
     f.close()
 
     f = open( sys.argv[2] )
     t = int(f.readline())
     t = 1
     for l in f:
         a,b = [int(x) for x in l.split()]
         mt = sqpals >= a
         lt = sqpals <= b
         output = sum( mt&lt )
         print "Case #%s: %s"%(t,output)
         t += 1
     
