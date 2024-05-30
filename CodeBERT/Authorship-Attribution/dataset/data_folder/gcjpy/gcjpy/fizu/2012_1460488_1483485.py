from codejam import *
 from string import maketrans
 
 inp = "ejp mysljylc kd kxveddknmc re jsicpdrysi"\
       "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd"\
       "de kr kd eoya kw aej tysr re ujdr lkgc jv zq"
 out = "our language is impossible to understand"\
     "there are twenty six factorial possibilities"\
     "so it is okay if you want to just give up qz"
 
 for case in xrange(readint()):
     trantab = maketrans(inp, out)
     line = readstring()
     print "Case #%d: %s" % (case + 1, line.translate(trantab))
