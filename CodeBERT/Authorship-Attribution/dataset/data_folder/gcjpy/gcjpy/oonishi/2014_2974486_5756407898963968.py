# coding: cp932
 
 #input = open(r'C:\MyDocument\home\gcj\2014-04-12\a.sample')
 input = open(r'C:\MyDocument\home\gcj\2014-04-12\A-small-attempt0.in')
 caseCnt = int(input.readline())
 for caseNo in range(1, caseCnt+1):
 	ans1 = int(input.readline())
 	for i in range(1, 5):
 		line = input.readline()
 		if ans1 == i:
 			candidates = set(map(int, line.split()))
 		
 	ans2 = int(input.readline())
 	for i in range(1, 5):
 		line = input.readline()
 		if ans2 == i:
 			answers = candidates.intersection(set(map(int, line.split())))
 		
 	if len(answers) == 0:
 		print('Case #%d: Volunteer cheated!'%caseNo)
 	elif len(answers) > 1:
 		print('Case #%d: Bad magician!'%caseNo)
 	elif len(answers) == 1:
 		answer = answers.pop()
 		print('Case #%d: %d'%(caseNo, answer))
