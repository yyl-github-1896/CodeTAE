T = int(raw_input());
 for q in range(T):
     [C,F,X] = map(float, raw_input().split());
 
     # Default rate is 2 cookies / s;
     # Farm costs C
     #   produces F
     # Target is X;
 
     Time = 0.;
     Rate = 2.;
     Fin = False;
     while (not Fin):
         t0 = X/Rate;
         t1 = C/Rate + X/(Rate+F);
 
         if t0 <= t1:
             Time += t0;
             Fin = True;
         else:
             Time += C/Rate;
             Rate += F;
 
     print "Case #%d:" % (q+1),;
     print "%.7f" % Time;
     
         
