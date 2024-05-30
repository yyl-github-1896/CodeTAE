t = int(raw_input())
 
 max = [0, 1, 1, 2, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6, 5, 6, 7, 6, 7, 8, 7, 8, 9, 8, 9, 10, 9, 10, 10, 10]
 
 for i in range(t):
 	line = raw_input().split(' ')
 	n = int(line[0])
 	s = int(line[1])
 	p = int(line[2])
 
 	total = 0
 
 	for j in range(3, len(line)):
 		t = int(line[j])
 		if t == 0:
 			if p == 0:
 				total += 1
 		elif t%3 == 0:
 			if t/3 >= p:
 				total +=1
 			elif t/3 + 1 >= p and s>0:
 				total +=1
 				s -=1
 		elif t%3 == 1:
 			if (t+2)/3 >= p:
 				total +=1
 		else:
 			if (t+1)/3 >= p:
 				total +=1
 			elif (t+1)/3 + 1 >= p and s>0:
 				total +=1
 				s -=1
 
 
 
 	print 'Case #'+str(i+1)+':', total
 
 
