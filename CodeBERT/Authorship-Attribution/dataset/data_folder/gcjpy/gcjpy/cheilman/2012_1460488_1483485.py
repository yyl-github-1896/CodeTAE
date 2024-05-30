#!/usr/bin/python
 
 from string import maketrans
 
 input = "aoz"
 outpt = "yeq"
 
 input = input + "our language is impossible to understand"
 outpt = outpt + "ejp mysljylc kd kxveddknmc re jsicpdrysi"
 
 input = input + "there are twenty six factorial possibilities"
 outpt = outpt + "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd"
 
 input = input + "so it is okay if you want to just give up"
 outpt = outpt + "de kr kd eoya kw aej tysr re ujdr lkgc jv"
 
 input = input + "q"
 outpt = outpt + "z"
 
 togoog = maketrans(input, outpt)
 ungoog = maketrans(outpt, input)
 
 filename = "A-small-attempt1.in"
 
 file = open(filename, "rt")
 
 T = int(file.readline().strip())
 
 for i in xrange(T):
 	line = file.readline().strip()
 
 	print "Case #%d: %s" % (i + 1, line.translate(ungoog))
