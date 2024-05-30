T = int(raw_input());
 for case in range(T):
    [A,B] = map(int, raw_input().split());
 
    Big = 10**(len(str(A))-1);
    Ans = 0;
 
    for i in range(A,B+1):
       j = (i/10)+Big*(i%10);
       while (j != i):
          if i < j <= B:
             Ans += 1;
          j = (j/10)+Big*(j%10);
 
    print "Case #%d:" % (case+1),;
    print Ans;
    
 
