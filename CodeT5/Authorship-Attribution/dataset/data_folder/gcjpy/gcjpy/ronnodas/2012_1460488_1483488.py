T=int(input())
 for t in range(T):
     a,b = [int(x) for x in input().split()]
     count = 0
     l = [0 for i in range(a,b+1)]
     for n in range(a,b):
         if l[n-a]:
             continue
         l[n-a]=1
         ms = set()
         s = str(n)
         for i in range(len(s)):
             m = int(s[i:]+s[:i])
             if n<m<=b:
                 l[m-a]=1
                 ms.add(m)
         case = len(ms)
         count+= (case*(case+1))//2
     print('Case #',t+1,': ',count,sep = '')
