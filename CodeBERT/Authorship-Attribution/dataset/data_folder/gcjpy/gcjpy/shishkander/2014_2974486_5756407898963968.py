def CASE(IN):
     def rstr(): return IN.readline().strip()
     def rint(): return int(rstr())
     def rints(): return map(int, rstr().split())
     def rr():
         x = rint()
         m = [rints() for i in xrange(4)]
         return set(m[x-1])
     s = rr().intersection(rr())
     if not s:
         return "Volunteer cheated!"
     if len(s) == 1:
         return s.pop()
     return "Bad magician!"
 
 
 def RUN(IN, OUT):
     t = int(IN.readline().strip())
     for i in xrange(1,t+1):
         OUT.write("Case #%i: %s\n" % (i, CASE(IN)))
 
 if __name__ == "__main__":
     import sys
     RUN(sys.stdin, sys.stdout)
