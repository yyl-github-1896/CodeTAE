import sys
 
 def play_war(b1, b2):
 	if 0 == len(b1):
 		return 0
 		
 	if b1[0] > b2[0]:
 		b1.pop(0)
 		b2.pop()
 		return 1 + play_war(b1, b2)
 	else:
 		b1.pop(0)
 		b2.pop(0)
 		return play_war(b1, b2)
 		
 def play_deceitful_war(b1, b2):
 	if 0 == len(b1):
 		return 0
 		
 	i = len(b1) - 1
 	while (i >= 0) and (b1[i] < b2[len(b2) - 1]):
 		i -= 1
 		
 	if i < 0:
 		return 0
 	
 	
 	b1.pop(i)
 	b2.pop()
 
 	return 1 + play_deceitful_war(b1, b2)
 
 
 t = int(sys.stdin.readline().strip())
 
 for i in range(t):
 	print "Case #" + str(i + 1) + ":",
 
 	n = int(sys.stdin.readline().strip())
 	
 	blocks1 = sorted([float(j) for j in sys.stdin.readline().strip().split()], reverse = True)
 	blocks2 = sorted([float(j) for j in sys.stdin.readline().strip().split()], reverse = True)
 
 	print play_deceitful_war(list(blocks1), list(blocks2)), play_war(blocks1, blocks2)
 	
