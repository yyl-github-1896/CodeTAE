# Making up a dictionary
 # Sample
 googlerese = "ejp mysljylc kd kxveddknmc re jsicpdrysi rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd de kr kd eoya kw aej tysr re ujdr lkgc jv"
 english = "our language is impossible to understand there are twenty six factorial possibilities so it is okay if you want to just give up"
 # Hints
 d = {"y":"a", "e":"o", "q":"z"}
 
 for i in xrange(len(googlerese)):
 	d[googlerese[i]] = english[i]
 
 # One letter still missing: z:q
 d["z"] = "q"
 
 inp = file("input.in")
 n = eval(inp.readline())
 out = file("output.txt", "w")
 
 for i in xrange(n):
 	G = inp.readline().strip()
 	S = ""
 	for letter in G:
 		S += d[letter]
 	out.write("Case #%d: " %(i + 1) + S + "\n")
