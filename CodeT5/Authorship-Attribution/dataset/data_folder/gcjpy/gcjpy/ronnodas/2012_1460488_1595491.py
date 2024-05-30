T=int(input())
 for t in range(T):
   l = [int(x) for x in input().split()]
   n,huh,p = l[:3]
   ss = l[3:]
   nice, maybe = 0,0
   for s in ss:
     if s>= p+2*max(p-1,0):
       nice += 1
     elif s>= p+2*max(p-2,0):
       maybe += 1
   y = nice + min(maybe,huh)
   print('Case #',t+1,': ',y,sep = '')
 
 
