import sys
 import math
 
 def is_square(n):
     if n in square:
         return True
     if is_fair(n):
         root = int(math.sqrt(n))
         if root**2 != n:
             return False
         ss = is_fair(root)
         if ss: square.add(n)
         return ss
     return False
 
 def is_fair(n):
     if n in fair:
         return True
     if n in unfair:
         return False
     sn = str(n)
     l = len(sn)
     mid = math.ceil(n/2)
     if sn[0:mid] == sn[mid::-1]:
         fair.add(n)
         return True
     else:
         unfair.add(n)
         return False
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
             
     fair = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 11])
     unfair = set([12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
     square = set([1, 4])
 
     t = int(f.readline())
     for _t in range(t):
         s = f.readline()
         if s:
             x, y = s.split()
             Total = sum([is_square(n) for n in range(int(x), int(y)+1)])             
             print ("Case #" + str(_t+1) + ": " + str(Total))
     
 
