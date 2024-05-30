mapp = {' ': ' ', 'a': 'y', 'c': 'e', 'b': 'h', 'e': 'o', 'd': 's', 'g': 'v', 'f': 'c', 'i': 'd', 'h': 'x', 'k': 'i', 'j': 'u', 'm': 'l', 'l': 'g', 'o': 'k', 'n': 'b', 'p': 'r', 's': 'n', 'r': 't', 'u': 'j', 't': 'w', 'w': 'f', 'v': 'p', 'y': 'a', 'x': 'm','q':'z','z':'q'}
 input = open("A-small-attempt0.in", "rU").readlines()
 counter = 0
 for a in input[1:]:
 	counter += 1
 	outline = a.replace("\n",'')
 	outline2 = []
 	for i in outline:
 		outline2.append(mapp[i])
 	print ("Case #"+str(counter)+":",''.join(outline2))
 
