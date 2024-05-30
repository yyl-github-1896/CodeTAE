import sys
 
 def all_grids(R,C,M, lp=0,placed=0):
     rem = R*C-lp
     if M-placed >= rem:
         if M-placed > rem:
             return None
         
         res = set()
         for i in range(lp, R*C):
             res.add(i)
         return [res]
         
     if placed == M:
         return [set()]
 
     res = []
     for i in range(lp, R*C):
         sub_sol = all_grids(R,C,M,i+1, placed+1)
         if sub_sol is None:
             continue
             
         for s in sub_sol:
             s.add(i)
             res.append(s)
     return res
 
 def adj(R,C,i):
     
     res = []
     left_edge = i % C == 0
     top_edge = i // C == 0
     right_edge = (i+1) % C == 0
     bottom_edge = i // C == R-1
     
     if not left_edge:
         res.append(i-1)
         if not top_edge:
             res.append(i-1-C)
         if not bottom_edge:
             res.append(i+C-1)
             
     if not right_edge:
         res.append(i+1)
         if not top_edge:
             res.append(i+1-C)
         if not bottom_edge:
             res.append(i+1+C)
             
     if not bottom_edge:
         res.append(i+C)
     if not top_edge:
         res.append(i-C)
     return res
         
     
     
     
 def solution(R,C,g):
     M = R*C
     res = []
     num_zeroes = 0
     for i in range(M):
         if i in g:
             res.append('x')
             continue
         x = 0
         for a in adj(R,C,i):
             if a in g:
                 x += 1
         if x == 0:
             num_zeroes += 1
         res.append(x)
         
     for i in range(M):
         if i in g:
             continue
         r = res[i]
         if r == 0 and num_zeroes == 1:
             continue
         connected = False
         for a in adj(R,C,i):
             if res[a] == 0:
                 connected = True
                 break
         if not connected:
             return None
     
     return res.index(0)
 
 def transcribe(R,C, g, sol):
     res = []
     for i in range(R):
         r = []
         for j in range(C):
             x = i*C+j
             if x in g:
                 r.append('*')
             elif x == sol:
                 r.append('c')
             else:
                 r.append('.')
         res.append(r)
     return res
 
 def printed_sol(transcript):
     if transcript is None:
         return "Impossible"
     else:
         return "\n".join("".join(row) for row in transcript)
 
 def solve(R,C,M):
     if M == R*C-1:
         g = []
         for i in range(R*C-1):
             g.append(i)
         return transcribe(R,C, g, R*C-1)
     
     for g in all_grids(R,C,M):
         sol = solution(R,C,g)
         if sol is None:
             continue
         return transcribe(R,C, g, sol)
     return None
             
     
 def output_grid(R,C,g):
     for i in range(R):
         for j in range(C):
             if i*C+j not in g:
                 sys.stdout.write(".")
             else:
                 sys.stdout.write("*")
         sys.stdout.write("\n")
 
 if __name__ == "__main__":
     T = int(raw_input())
     for i in range(1,T+1):
         R,C,M = map(int, raw_input().split())
         print "Case #%d:" % i
         print printed_sol(solve(R,C,M))
