t = int(raw_input())
 
 for case in range(t):
 	r1 = int(raw_input())
 	c1 = []
 	for j in range(4):
 		c1.append([int(i) for i in raw_input().split()])
 
 	r2 = int(raw_input())
 	c2 = []
 	for j in range(4):
 		c2.append([int(i) for i in raw_input().split()])
 
 	num = -1
 	possibles = 0
 	for j in c1[r1-1]:
 		if c2[r2-1].count(j) == 1:
 			num = j
 			possibles += 1
 
 	if possibles > 1:
 		print 'Case #'+str(case+1)+': Bad magician!'
 	elif possibles == 0:
 		print 'Case #'+str(case+1)+': Volunteer cheated!'
 	else:
 		print 'Case #'+str(case+1)+': '+str(num)
