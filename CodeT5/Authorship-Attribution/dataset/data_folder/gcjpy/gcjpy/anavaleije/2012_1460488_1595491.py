arq = file("input.in")
 n_cases = eval(arq.readline())
 out = file("output.txt", "w")
 
 for case in xrange(n_cases):
 
 	data = arq.readline()
 	data = data.strip()
 	data = data.split(" ")
 
 	n = eval(data[0])
 	s = eval(data[1])
 	p = eval(data[2])
 
 	scores = []
 	n_googlers_with_best_result = 0
 	candidates = 0
 
 	for j in data[3:]:
 		i = eval(j)
 		if i%3 == 0:
 			score = i/3
 			scores.append([score, score, score])
 		elif (i+1)%3 == 0:
 			score = (i+1)/3
 			scores.append([score-1, score, score])
 		else: #(i+2)%3 == 0
 			score = (i+2)/3
 			scores.append([score-1, score-1, score])
 
 	for score in scores:
 		if score[2] >= p:
 			n_googlers_with_best_result +=1
 		elif score[2] + 1 == p and score[1] == score[2] and score[2] != 0:
 			candidates += 1
 
 	n_googlers_with_best_result = n_googlers_with_best_result + min(s, candidates)
 
 	out.write("Case #%d: %d\n" % (case+1, n_googlers_with_best_result))
