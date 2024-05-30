def esPal(x):
 	return str(x) == str(x)[::-1]
 
 t = int(raw_input())
 
 for case in range(t):
 	line = raw_input().split(' ')
 	a = int(line[0])
 	b = int(line[1])
 
 	i = int(a**.5)
 	if i*i != a:
 		i += 1
 	max = int(b**.5)
 	cantidad = 0
 	while i <= max:
 		if esPal(i) and esPal(i*i):
 			cantidad += 1
 		i += 1
 
 	print 'Case #'+str(case+1)+':', cantidad
