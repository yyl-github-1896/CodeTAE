import sys
 
 def decode_data(input, x, y, z):
     rotated = zip(*input[::-1])
     #for row in rotated:
         #print (row)
     #for row in input:
         #print (row)
     for i in range(x):
         for j in range(y):
             if not input[i][j] == "1":
                 continue            
             if sum((int(xx) for xx in input[i])) != y and \
                sum((int(xx) for xx in rotated[j])) != x:
                 return "NO"
     return "YES"
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())
     for _t in range(t):
         x, y = f.readline().split()
         s = [f.readline().split() for i in range(int(x))]
         print ("Case #" + str(_t+1) + ": " + decode_data(s, int(x), int(y), 2))
     
 
