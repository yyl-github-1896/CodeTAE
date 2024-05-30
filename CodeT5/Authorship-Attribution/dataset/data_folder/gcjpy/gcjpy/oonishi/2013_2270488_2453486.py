# coding: cp932
 import sys
 f   = file(sys.argv[1])
 out = file(sys.argv[2], 'w')
 
 caseCnt = int(f.readline())
 
 for case in range(1, caseCnt+1):
 	board = [
 		f.readline()[:4],
 		f.readline()[:4],
 		f.readline()[:4],
 		f.readline()[:4],
 	]
 	f.readline()
 	xwin = False
 	owin = False
 	rest = False
 	# 
 	for row in board:
 		if row.replace('T', 'X') == 'XXXX':
 			xwin = True
 		elif row.replace('T', 'O') == 'OOOO':
 			owin = True
 		if '.' in row: rest = True
 	# c
 	for i in range(4):
 		col = ''.join([row[i] for row in board])
 		if col.replace('T', 'X') == 'XXXX':
 			xwin = True
 		elif col.replace('T', 'O') == 'OOOO':
 			owin = True
 	# ȂȂ
 	up = ''.join([row[i] for i, row in enumerate(board)])
 	if up.replace('T', 'X') == 'XXXX':
 		xwin = True
 	elif up.replace('T', 'O') == 'OOOO':
 		owin = True
 	down = ''.join([row[3-i] for i, row in enumerate(board)])
 	if down.replace('T', 'X') == 'XXXX':
 		xwin = True
 	elif down.replace('T', 'O') == 'OOOO':
 		owin = True
 	
 	assert not (xwin==owin==True)
 	
 	if xwin:
 		result = 'X won'
 	elif owin:
 		result = 'O won'
 	elif rest:
 		result = 'Game has not completed'
 	else:
 		result = 'Draw'
 		
 	print>>out, 'Case #%d:'%case, result
 
 out.close()
