t = int(raw_input())
 
 code = 'yhesocvxduiglbkrztnwjpfmaq'
 
 for i in range(t):
 	l = []
 	for j in range(4):
 		l.append(raw_input())
 	if i != t-1:
 		raw_input()
 
 	# filas
 	v = False
 	fin = False
 	for li in l:
 		x = True
 		o = True
 		for c in li:
 			if c != 'X' and c != 'T':
 				x = False
 			if c != 'O' and c != 'T':
 				o = False
 			if c == '.':
 				v = True
 		if x:
 			print 'Case #'+str(i+1)+': X won'
 			fin = True
 		if o:
 			print 'Case #'+str(i+1)+': O won'
 			fin = True
 
 	if fin:
 		continue
 
 	#columnas
 	for a in range(4):
 		x = True
 		o = True
 		for b in range(4):
 			if l[b][a] != 'X' and l[b][a] != 'T':
 				x = False
 			if l[b][a] != 'O' and l[b][a] != 'T':
 				o = False
 		if x:
 			print 'Case #'+str(i+1)+': X won'
 			fin = True
 		if o:
 			print 'Case #'+str(i+1)+': O won'
 			fin = True
 	if fin:
 		continue
 
 	#diagonales
 	x = True
 	o = True
 	for j in range(4):
 		if l[j][j] != 'X' and l[j][j] != 'T':
 			x = False
 		if l[j][j] != 'O' and l[j][j] != 'T':
 			o = False
 	if x:
 		print 'Case #'+str(i+1)+': X won'
 		continue
 	if o:
 		print 'Case #'+str(i+1)+': O won'
 		continue
 	x = True
 	o = True
 	for j in range(4):
 		if l[3-j][j] != 'X' and l[3-j][j] != 'T':
 			x = False
 		if l[3-j][j] != 'O' and l[3-j][j] != 'T':
 			o = False
 	if x:
 		print 'Case #'+str(i+1)+': X won'
 		continue
 	if o:
 		print 'Case #'+str(i+1)+': O won'
 		continue
 
 	if v:
 		print 'Case #'+str(i+1)+': Game has not completed'
 	else:
 		print 'Case #'+str(i+1)+': Draw'
