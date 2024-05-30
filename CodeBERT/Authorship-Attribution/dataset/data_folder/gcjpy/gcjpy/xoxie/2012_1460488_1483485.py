import string
 
 s1 = "ejp mysljylc kd kxveddknmc re jsicpdrysi rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcdde kr kd eoya kw aej tysr re ujdr lkgc jvyeqz"
 s2 = "our language is impossible to understand there are twenty six factorial possibilitiesso it is okay if you want to just give upaozq"
 
 mapd = string.maketrans(s1,s2)
 #print "abcdefghijklmnopqrstuvwxyz"
 #print "abcdefghijklmnopqrstuvwxyz".translate(mapd)
 
 f = open( "A-small-attempt0.in.txt" )
 g = open( "output_small.txt","w")
 
 f.readline()
 l = f.readline()
 caseI = 1
 while l != "":
     output = l.translate(mapd)
 
     g.write( "Case #%s: %s"%(caseI,output) )
     l = f.readline()
     caseI += 1
 f.close()
 g.close()
