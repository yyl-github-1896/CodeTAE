def solve(c1, g1, c2, g2):
     row_1 = g1[c1-1]
     row_2 = g2[c2-1]
     inter = set(row_1) & set(row_2)
     if len(inter) == 0:
         return "Volunteer cheated!"
     if len(inter) > 1:
         return "Bad magician!"
     return str(inter.pop())
 
 if __name__ == "__main__":
     T = int(raw_input())
     for i in range(1,T+1):
         c1 = int(raw_input())
         g1 = []
         for j in range(4):
             g1.append(map(int, raw_input().split()))
         c2 = int(raw_input())
         g2 = []
         for j in range(4):
             g2.append(map(int, raw_input().split()))
         print "Case #%d: %s" % (i, solve(c1,g1,c2,g2)) 
         
     
