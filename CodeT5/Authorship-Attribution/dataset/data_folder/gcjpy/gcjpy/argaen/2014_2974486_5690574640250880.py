t = int(raw_input())
 
 for case in range(t):
 	print 'Case #'+str(case+1)+':'
 	r, c, m = raw_input().split()
 	r = int(r)
 	c = int(c)
 	m = int(m)
 
 	if m==0:
 		print 'c' + ('.'*(c-1))
 		for i in range(r-1):
 			print '.'*c
 	elif r == 1:
 		print 'c'+('.'*(c-m-1))+('*'*(m))
 	elif c == 1:
 		print 'c'
 		for i in range(r-m-1):
 			print '.'
 		for i in range(m):
 			print '*'
 	elif r == 2:
 		if m%2==0 and c>2 and m<r*c-2:
 			print 'c'+('.'*(c-m/2-1))+('*'*(m/2))
 			print ('.'*(c-m/2))+('*'*(m/2))
 		elif m == r*c - 1:
 			print 'c'+('*'*(c-1))
 			print '*'*c
 		else:
 			print 'Impossible'
 	elif c == 2:
 		if m%2==0 and r>2 and m<r*c-2:
 			print 'c.'
 			for i in range(r-m/2-1):
 				print '..'
 			for i in range(m/2):
 				print '**'
 		elif m == r*c - 1:
 			print 'c*'
 			for i in range(r-1):
 				print '**'
 		else:
 			print 'Impossible'
 	elif c == 3 and r == 3:
 		if m == 1:
 			print 'c..'
 			print '...'
 			print '..*'
 		elif m == 2:
 			print 'Impossible'
 		elif m == 3:
 			print 'c..'
 			print '...'
 			print '***'
 		elif m == 4:
 			print 'Impossible'
 		elif m == 5:
 			print 'c.*'
 			print '..*'
 			print '***'
 		elif m == 6:
 			print 'Impossible'
 		elif m == 7:
 			print 'Impossible'
 		elif m == 8:
 			print 'c**'
 			print '***'
 			print '***'
 	elif c == 3 and r == 4:
 		if m == 1:
 			print 'c..'
 			print '...'
 			print '...'
 			print '..*'
 		elif m == 2:
 			print 'c..'
 			print '...'
 			print '..*'
 			print '..*'
 		elif m == 3:
 			print 'c..'
 			print '...'
 			print '...'
 			print '***'
 		elif m == 4:
 			print 'c.*'
 			print '..*'
 			print '..*'
 			print '..*'
 		elif m == 5:
 			print 'Impossible'
 		elif m == 6:
 			print 'c..'
 			print '...'
 			print '***'
 			print '***'
 		elif m == 7:
 			print 'Impossible'
 		elif m == 8:
 			print 'c.*'
 			print '..*'
 			print '***'
 			print '***'
 		elif m == 9:
 			print 'Impossible'
 		elif m == 10:
 			print 'Impossible'
 		elif m == 11:
 			print 'c**'
 			print '***'
 			print '***'
 			print '***'
 	elif c == 3 and r == 5:
 		if m == 1:
 			print 'c..'
 			print '...'
 			print '...'
 			print '...'
 			print '..*'
 		elif m == 2:
 			print 'c..'
 			print '...'
 			print '...'
 			print '..*'
 			print '..*'
 		elif m == 3:
 			print 'c..'
 			print '...'
 			print '..*'
 			print '..*'
 			print '..*'
 		elif m == 4:
 			print 'c..'
 			print '...'
 			print '...'
 			print '..*'
 			print '***'
 		elif m == 5:
 			print 'c.*'
 			print '..*'
 			print '..*'
 			print '..*'
 			print '..*'
 		elif m == 6:
 			print 'c..'
 			print '...'
 			print '...'
 			print '***'
 			print '***'
 		elif m == 7:
 			print 'c..'
 			print '...'
 			print '..*'
 			print '***'
 			print '***'
 		elif m == 8:
 			print 'Impossible'
 		elif m == 9:
 			print 'c..'
 			print '...'
 			print '***'
 			print '***'
 			print '***'
 		elif m == 10:
 			print 'Impossible'
 		elif m == 11:
 			print 'c.*'
 			print '..*'
 			print '***'
 			print '***'
 			print '***'
 		elif m == 12:
 			print 'Impossible'
 		elif m == 13:
 			print 'Impossible'
 		elif m == 14:
 			print 'c**'
 			print '***'
 			print '***'
 			print '***'
 			print '***'
 	elif c == 4 and r == 3:
 		if m == 1:
 			print 'c...'
 			print '....'
 			print '...*'
 		elif m == 2:
 			print 'c...'
 			print '...*'
 			print '...*'
 		elif m == 3:
 			print 'c..*'
 			print '...*'
 			print '...*'
 		elif m == 4:
 			print 'c...'
 			print '....'
 			print '****'
 		elif m == 5:
 			print 'Impossible'
 		elif m == 6:
 			print 'c.**'
 			print '..**'
 			print '..**'
 		elif m == 7:
 			print 'Impossible'
 		elif m == 8:
 			print 'c.**'
 			print '..**'
 			print '****'
 		elif m == 9:
 			print 'Impossible'
 		elif m == 10:
 			print 'Impossible'
 		elif m == 11:
 			print 'c***'
 			print '****'
 			print '****'
 	elif c == 4 and r == 4:
 		if m == 1:
 			print 'c...'
 			print '....'
 			print '....'
 			print '...*'
 		elif m == 2:
 			print 'c...'
 			print '....'
 			print '....'
 			print '..**'
 		elif m == 3:
 			print 'c...'
 			print '....'
 			print '...*'
 			print '..**'
 		elif m == 4:
 			print 'c...'
 			print '....'
 			print '....'
 			print '****'
 		elif m == 5:
 			print 'c...'
 			print '....'
 			print '...*'
 			print '****'
 		elif m == 6:
 			print 'c...'
 			print '....'
 			print '..**'
 			print '****'
 		elif m == 7:
 			print 'c..*'
 			print '...*'
 			print '...*'
 			print '****'
 		elif m == 8:
 			print 'c...'
 			print '....'
 			print '****'
 			print '****'
 		elif m == 9:
 			print 'Impossible'
 		elif m == 10:
 			print 'c.**'
 			print '..**'
 			print '..**'
 			print '****'
 		elif m == 11:
 			print 'Impossible'
 		elif m == 12:
 			print 'c.**'
 			print '..**'
 			print '****'
 			print '****'
 		elif m == 13:
 			print 'Impossible'
 		elif m == 14:
 			print 'Impossible'
 		elif m == 15:
 			print 'c***'
 			print '****'
 			print '****'
 			print '****'
 	elif c == 4 and r == 5:
 		if m == 1:
 			print 'c...'
 			print '....'
 			print '....'
 			print '....'
 			print '...*'
 		elif m == 2:
 			print 'c...'
 			print '....'
 			print '....'
 			print '....'
 			print '..**'
 		elif m == 3:
 			print 'c...'
 			print '....'
 			print '...*'
 			print '...*'
 			print '...*'
 		elif m == 4:
 			print 'c...'
 			print '....'
 			print '....'
 			print '....'
 			print '****'
 		elif m == 5:
 			print 'c..*'
 			print '...*'
 			print '...*'
 			print '...*'
 			print '...*'
 		elif m == 6:
 			print 'c...'
 			print '....'
 			print '....'
 			print '..**'
 			print '****'
 		elif m == 7:
 			print 'c..*'
 			print '...*'
 			print '...*'
 			print '..**'
 			print '..**'
 		elif m == 8:
 			print 'c...'
 			print '....'
 			print '....'
 			print '****'
 			print '****'
 		elif m == 9:
 			print 'c..*'
 			print '...*'
 			print '...*'
 			print '..**'
 			print '****'
 		elif m == 10:
 			print 'c.**'
 			print '..**'
 			print '..**'
 			print '..**'
 			print '..**'
 		elif m == 11:
 			print 'c..*'
 			print '...*'
 			print '...*'
 			print '****'
 			print '****'
 		elif m == 12:
 			print 'c...'
 			print '....'
 			print '****'
 			print '****'
 			print '****'
 		elif m == 13:
 			print 'Impossible'
 		elif m == 14:
 			print 'c..*'
 			print '...*'
 			print '****'
 			print '****'
 			print '****'
 		elif m == 15:
 			print 'Impossible'
 		elif m == 16:
 			print 'c.**'
 			print '..**'
 			print '****'
 			print '****'
 			print '****'
 		elif m == 17:
 			print 'Impossible'
 		elif m == 18:
 			print 'Impossible'
 		elif m == 19:
 			print 'c***'
 			print '****'
 			print '****'
 			print '****'
 			print '****'
 	elif c == 5 and r == 3:
 		if m == 1:
 			print 'c....'
 			print '.....'
 			print '....*'
 		elif m == 2:
 			print 'c....'
 			print '.....'
 			print '...**'
 		elif m == 3:
 			print 'c....'
 			print '.....'
 			print '..***'
 		elif m == 4:
 			print 'c...*'
 			print '....*'
 			print '...**'
 		elif m == 5:
 			print 'c....'
 			print '.....'
 			print '*****'
 		elif m == 6:
 			print 'c..**'
 			print '...**'
 			print '...**'
 		elif m == 7:
 			print 'c..**'
 			print '...**'
 			print '..***'
 		elif m == 8:
 			print 'Impossible'
 		elif m == 9:
 			print 'c.***'
 			print '..***'
 			print '..***'
 		elif m == 10:
 			print 'Impossible'
 		elif m == 11:
 			print 'c.***'
 			print '..***'
 			print '*****'
 		elif m == 12:
 			print 'Impossible'
 		elif m == 13:
 			print 'Impossible'
 		elif m == 14:
 			print 'c****'
 			print '*****'
 			print '*****'
 	elif c == 5 and r == 4:
 		if m == 1:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '....*'
 		elif m == 2:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '...**'
 		elif m == 3:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '..***'
 		elif m == 4:
 			print 'c...*'
 			print '....*'
 			print '....*'
 			print '....*'
 		elif m == 5:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '*****'
 		elif m == 6:
 			print 'c...*'
 			print '....*'
 			print '....*'
 			print '..***'
 		elif m == 7:
 			print 'c....'
 			print '.....'
 			print '...**'
 			print '*****'
 		elif m == 8:
 			print 'c..**'
 			print '...**'
 			print '...**'
 			print '...**'
 		elif m == 9:
 			print 'c...*'
 			print '....*'
 			print '...**'
 			print '*****'
 		elif m == 10:
 			print 'c....'
 			print '.....'
 			print '*****'
 			print '*****'
 		elif m == 11:
 			print 'c..**'
 			print '...**'
 			print '...**'
 			print '*****'
 		elif m == 12:
 			print 'c.***'
 			print '..***'
 			print '..***'
 			print '..***'
 		elif m == 13:
 			print 'Impossible'
 		elif m == 14:
 			print 'c.***'
 			print '..***'
 			print '..***'
 			print '*****'
 		elif m == 15:
 			print 'Impossible'
 		elif m == 16:
 			print 'c.***'
 			print '..***'
 			print '*****'
 			print '*****'
 		elif m == 17:
 			print 'Impossible'
 		elif m == 18:
 			print 'Impossible'
 		elif m == 19:
 			print 'c****'
 			print '*****'
 			print '*****'
 			print '*****'
 	elif c == 5 and r == 5:
 		if m == 1:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '.....'
 			print '....*'
 		elif m == 2:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '.....'
 			print '...**'
 		elif m == 3:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '.....'
 			print '..***'
 		elif m == 4:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '...**'
 			print '...**'
 		elif m == 5:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '.....'
 			print '*****'
 		elif m == 6:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '..***'
 			print '..***'
 		elif m == 7:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '...**'
 			print '*****'
 		elif m == 8:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '..***'
 			print '*****'
 		elif m == 9:
 			print 'c...*'
 			print '....*'
 			print '....*'
 			print '....*'
 			print '*****'
 		elif m == 10:
 			print 'c....'
 			print '.....'
 			print '.....'
 			print '*****'
 			print '*****'
 		elif m == 11:
 			print 'c....'
 			print '.....'
 			print '....*'
 			print '*****'
 			print '*****'
 		elif m == 12:
 			print 'c....'
 			print '.....'
 			print '...**'
 			print '*****'
 			print '*****'
 		elif m == 13:
 			print 'c....'
 			print '.....'
 			print '..***'
 			print '*****'
 			print '*****'
 		elif m == 14:
 			print 'c..**'
 			print '...**'
 			print '...**'
 			print '..***'
 			print '*****'
 		elif m == 15:
 			print 'c....'
 			print '.....'
 			print '*****'
 			print '*****'
 			print '*****'
 		elif m == 16:
 			print 'c..**'
 			print '...**'
 			print '...**'
 			print '*****'
 			print '*****'
 		elif m == 17:
 			print 'c..**'
 			print '...**'
 			print '..***'
 			print '*****'
 			print '*****'
 		elif m == 18:
 			print 'Impossible'
 		elif m == 19:
 			print 'c..**'
 			print '...**'
 			print '*****'
 			print '*****'
 			print '*****'
 		elif m == 20:
 			print 'Impossible'
 		elif m == 21:
 			print 'c.***'
 			print '..***'
 			print '*****'
 			print '*****'
 			print '*****'
 		elif m == 22:
 			print 'Impossible'
 		elif m == 23:
 			print 'Impossible'
 		elif m == 24:
 			print 'c****'
 			print '*****'
 			print '*****'
 			print '*****'
 			print '*****'
 	else:
 		print 'Impossible'
 
