import sys
 
 googlerese = """
 y qee
 ejp mysljylc kd kxveddknmc re jsicpdrysi
 rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
 de kr kd eoya kw aej tysr re ujdr lkgc jv
 z
 """
 
 plain = """
 a zoo
 our language is impossible to understand
 there are twenty six factorial possibilities
 so it is okay if you want to just give up
 q
 """
 
 gtos = {}
 stog = {}
 
 for s,g in zip(plain, googlerese):
 	gtos[g] = s
 	stog[s] = g
 
 #for c in "abcdefghijklmnopqrstuvwxyz":
 #	print c, stog.get(c, None), gtos.get(c,None)
 
 f = sys.stdin
 
 t = int(f.readline())
 
 for i in xrange(0,t):
 	line = f.readline().strip()
 	print "Case #%d: %s" % (i+1, "".join([gtos.get(c,c) for c in line]))
 
