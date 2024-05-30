import sys
 
 def digits(number, base = 10):
   while number:
     yield number % base
     number //= base
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())    
     for _t in range(t):
         s = f.readline()
         s = s.split()
         A = int(s[0])
         B = int(s[1])
         score = 0
         #print (A, B, [x for x in range(A, B)][-1])
         for i in range(A, B):
             #print (A, B, [x for x in range(i+1, B+1)][-1])
             for j in range(i+1, B+1):
                 id = [d for d in digits(i)]
                 jd = [d for d in digits(j)]
                 if  sorted(id) == sorted(jd):
                     checklist = [jd[n:] + jd[:n] for n in range(len(id))]
                     if id in checklist:
                         score +=1
                     #print(checklist)
         print ("Case #" + str(_t+1) + ": " + str(score))
     
 
