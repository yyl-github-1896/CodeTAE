# coding: shift-jis
 
 a = "abcdefghijklmnopqrstuvwxyz"
 d = {}
 for c in a:
 	d[c] = "*"
 
 i = "ejp mysljylc kd kxveddknmc re jsicpdrysi"
 o = "our language is impossible to understand"
 for k, v in zip(i, o):
 	d[k] = v
 i = "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd"
 o = "there are twenty six factorial possibilities"
 for k, v in zip(i, o):
 	d[k] = v
 i = "de kr kd eoya kw aej tysr re ujdr lkgc jv"
 o = "so it is okay if you want to just give up"
 for k, v in zip(i, o):
 	d[k] = v
 
 
 i = "y qee"
 o = "a zoo"
 for k, v in zip(i, o):
 	d[k] = v
 d['z'] = 'q'
 import sys
 f = file("A-small-attempt1.in")
 #w = sys.stdout
 w = file("answer.txt", "w")
 cnt = int(f.readline()[:-1])
 for no in range(cnt):
 	i = f.readline()[:-1]
 	o = ""
 	for k in i:
 		o += d[k]
 	print>>w, "Case #%d:"%(no+1), o
 
 
