import sys
 
 if __name__ == "__main__":
 	f = open( sys.argv[1] )
 	int(f.readline())
 		
 	num = 1
 	l = f.readline()
 	while l != "":
 		row1 = int(l)
 		rows = [ f.readline() for x in range(4) ]
 		row1 = [int(x) for x in rows[row1-1].split()]
 
 		row2 = int(f.readline())
 		rows = [f.readline() for x in range(4)]
 		row2 = [int(x) for x in rows[row2-1].split()]
 
 		result = set(row1) & set(row2)
 		if len(result) == 1:
 			output = str(result.pop())
 		elif len(result) > 1:
 			output = "Bad magician!"
 		else:
 			output = "Volunteer cheated!"
 
 		print "Case #"+str(num)+": "+output
 		num += 1
 		l = f.readline()
 		