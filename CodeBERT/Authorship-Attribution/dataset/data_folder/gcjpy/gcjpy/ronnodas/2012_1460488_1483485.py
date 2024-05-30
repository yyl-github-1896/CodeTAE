sub = {}
 sub['y']='a'
 sub['e']='o'
 sub['q']='z'
 sub[' ']=' '
 sub['z'] = 'q'
 
 pairs = [('ejp mysljylc kd kxveddknmc re jsicpdrysi','our language is impossible to understand'), ('rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd','there are twenty six factorial possibilities'), ('de kr kd eoya kw aej tysr re ujdr lkgc jv','so it is okay if you want to just give up')]
 
 for (j,(a,b)) in enumerate(pairs):
   for i in range(len(a)):
     sub[a[i]] = b[i]
     #print(a[i],b[i])
 
 #print(''.join(sorted(sub.keys())))
 #print(''.join(sorted(sub.values())))
 
 T=int(input())
 for i in range(T):
   s = input().strip()
   new = ''.join([sub[c] for c in s])
   print('Case #',i+1,': ',new,sep = '')
 
 
