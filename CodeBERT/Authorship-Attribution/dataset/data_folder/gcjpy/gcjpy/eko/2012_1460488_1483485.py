import sys, os
 import re
 
 fLine = sys.stdin.readline().split()
 tCase = int(fLine[0])
 
 
 dic = {		'a':'y',
 			'b':'h',
 			'c':'e',
 			'd':'s',
 			'e':'o',
 			'f':'c',
 			'g':'v',
 			'h':'x',
 			'i':'d',
 			'j':'u',
 			'k':'i',
 			'l':'g',
 			'm':'l',
 			'n':'b',
 			'o':'k',
 			'p':'r',
 			'q':'z',
 			'r':'t',
 			's':'n',
 			't':'w',
 			'u':'j',
 			'v':'p',
 			'w':'f',
 			'x':'m',
 			'y':'a',
 			'z':'q',
 			'\n':'',
 			' ':' '}
 
 
 def alien(frase):
 	resul = ""
 	for c in frase:
 		resul += dic[c]
 
 	return resul
 
 
 
 frases = []
 for i in xrange(tCase):
 	frase = sys.stdin.readline().replace("\n","")
 	frases.append(frase)
 	
 
 for i in xrange(tCase):	
 	#case.append(frase)
 	print "Case #%d: %s" % (i+1, alien(frases[i]))
 	
 	
 
