# coding: cp932
 import sys
 f   = file(sys.argv[1])
 out = file(sys.argv[2], 'w')
 
 caseCnt = int(f.readline())
 
 for case in range(1, caseCnt+1):
 	V, H = f.readline().split()
 	V = int(V); H = int(H)
 	
 	field = [map(int, list(f.readline().split())) for _ in range(V)]
 	#print field
 	
 	rowMax = [max(row) for row in field]
 	colMax = [max([row[i] for row in field]) for i in range(H)]
 	#print rowMax, colMax
 		
 	result = 'YES'
 	for row in range(V):
 		for col in range(H):
 			if field[row][col] < rowMax[row] and field[row][col] < colMax[col]:
 				result = 'NO'
 				break
 		else:
 			continue
 		break
 	print>>out, 'Case #%d:'%case, result
 
 out.close()
