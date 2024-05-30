def IsPal(n):
     S = str(n);
     return S == S[::-1];
 
 
 def Gen():
     LIM = 10**14;
     N = 10**7;
     LIST = [];
     for i in range(1, N):
         if IsPal(i):
             if IsPal(i*i):
                 LIST.append(i);
     return LIST
 
 PP = Gen();
 #print 'Generated'
 
 T = int(raw_input());
 for q in range(1,T+1):
     [A,B] = map(int, raw_input().split());    
     ANS = 0;
     for i in range(len(PP)):
         if B >= PP[i]**2 >= A:
             ANS += 1;
     
     print "Case #%d: %d" %(q, ANS);
