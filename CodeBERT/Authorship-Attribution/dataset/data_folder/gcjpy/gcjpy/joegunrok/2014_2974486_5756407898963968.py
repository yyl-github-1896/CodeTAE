__author__ = 'jrokicki'
 
 import sys
 RL = lambda: sys.stdin.readline().strip()
 IA = lambda: map(int, RL().split(" "))
 LA = lambda: map(long, RL().split(" "))
 
 T = int(sys.stdin.readline())
 
 for CASE in range(T):
     g1 = IA()[0]-1
     board1 = []
     for i in range(4):
         board1.append(IA())
     g2 = IA()[0]-1
     board2 = []
     for i in range(4):
         board2.append(IA())
 
     r1 = board1[g1]
     r2 = board2[g2]
 
     answer = set(r1).intersection(r2)
     if len(answer) > 1:
         answer = "Bad magician!"
     elif len(answer) == 0:
         answer = "Volunteer cheated!"
     else:
         answer = list(answer)[0]
 
     print "Case #%d: %s" % (CASE+1, answer)
 
