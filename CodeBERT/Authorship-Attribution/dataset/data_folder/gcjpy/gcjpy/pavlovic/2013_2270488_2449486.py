import sys
 
 direction = [[0, 1], [1, 0]]
 
 t = int(sys.stdin.readline())
 for i in range(t):
 	line = sys.stdin.readline().strip().split()
 	n = int(line[0])
 	m = int(line[1])
 	field = []
 	for j in range(n):
 		line = [int(x) for x in sys.stdin.readline().strip().split()]
 		field.append(line)
 
 	possibleLawn = True
 	for j in range(n):
 		for k in range(m):
 			for direct in range(2):
 				coords = [j if (direct == 0) else 0, 0 if (direct == 0) else k]
 				possibleField = True
 				while (coords[0] < n) and (coords[1] < m):
 					if field[j][k] < field[coords[0]][coords[1]]:
 						possibleField = False
 					coords[0] += direction[direct][0]
 					coords[1] += direction[direct][1]
 
 				if possibleField:
 					break
 			else:
 				possibleLawn = False
 
 	print "Case #" + str(i + 1) + ": " + ('YES' if possibleLawn else 'NO')
 
