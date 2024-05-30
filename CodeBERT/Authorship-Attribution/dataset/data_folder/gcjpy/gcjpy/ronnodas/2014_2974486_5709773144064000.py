from decimal import Decimal
 
 T = int(input())
 for case in range(1,T+1):
     C,F,X = (Decimal(x) for x in input().split())
     
     ans = X/2
     time,rate = 0,2
     while True:
         if time >= ans:
             break
         ans = min(ans,(X/rate)+time)
         time,rate = time+(C/rate),rate+F
     print("Case #",case,": ",ans,sep = '')
