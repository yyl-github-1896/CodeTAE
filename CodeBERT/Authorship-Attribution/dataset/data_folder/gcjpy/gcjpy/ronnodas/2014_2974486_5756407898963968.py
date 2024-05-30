T = int(input())
 for case in range(1,T+1):
     row1 = int(input())
     for i in range(1,5):
         l = input()
         if i==row1:
             first = set(int(x) for x in l.split())
     row2 = int(input())
     for i in range(1,5):
         l = input()
         if i==row2:
             second = set(int(x) for x in l.split())
     poss = first & second
     if len(poss) ==0:
         ans = 'Volunteer cheated!'
     elif len(poss) >1:
         ans = 'Bad magician!'
     else:
         ans = min(poss)
     print("Case #",case,": ",ans,sep = '')
