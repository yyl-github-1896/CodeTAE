RAW = ['ejp mysljylc kd kxveddknmc re jsicpdrysi',
        'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd',
        'de kr kd eoya kw aej tysr re ujdr lkgc jv']
 ENG = ['our language is impossible to understand',
        'there are twenty six factorial possibilities',
        'so it is okay if you want to just give up'];
 
 New = [32]*128;
 Left = [];
 for c in range(97, 123):
    Left += [chr(c)];
 
 for i in range(3):
    for j in range(len(RAW[i])):
        x = ord(RAW[i][j]);
        if (New[x] == 32) and (x != 32):
           Left.remove(RAW[i][j]);
        New[x] = ord(ENG[i][j]);
 
 New[ord('q')] = ord('z');
 New[ord('z')] = ord('q');
 
 
 T = int(raw_input());
 for i in range(T):
    print "Case #%d:" % (i+1),;
    S_in = raw_input();
    S_out = '';
    for c in S_in:
       S_out += chr(New[ord(c)])
    print S_out
    
 
