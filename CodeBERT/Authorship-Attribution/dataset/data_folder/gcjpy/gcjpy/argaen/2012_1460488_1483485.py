t = int(raw_input())
 
 code = ['y', 'h', 'e', 's', 'o', 'c', 'v', 'x', 'd', 'u', 'i', 'g', 'l', 'b', 'k', 'r', 'z', 't', 'n', 'w', 'j', 'p', 'f', 'm', 'a', 'q']
 
 for i in range(t):
 	line = raw_input()
 	decoded = ''
 
 	for c in line:
 		if c==' ':
 			decoded += c
 		else:
 			decoded += code[ord(c)-97]
 
 	print 'Case #'+str(i+1)+':', decoded
