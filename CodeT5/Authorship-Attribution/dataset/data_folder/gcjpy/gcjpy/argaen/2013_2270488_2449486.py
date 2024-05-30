t = int(raw_input())
 
 for case in range(t):
 	line = raw_input().split(' ')
 	n = int(line[0])
 	m = int(line[1])
 
 	l = []
 	for j in range(n):
 		a = raw_input().split(' ')
 		b = []
 		for x in a:
 			b.append(int(x))
 		l.append(b)
 
 	# para cada valor, revisar que la fila o columna que lo contenga sea de alto menor o igual
 
 	cumple = True
 	for i in range(n):
 		for j in range(m):
 			col = True
 			fil = True
 			for x in range(n):
 				if l[x][j] > l[i][j]:
 					col = False
 					break
 			for x in range(m):
 				if l[i][x] > l[i][j]:
 					fil = False
 					break
 
 			if not col and not fil:
 				cumple = False
 				break
 
 		if not cumple:
 			break
 
 	if cumple:
 		print 'Case #'+str(case+1)+': YES'
 	else:
 		print 'Case #'+str(case+1)+': NO'
