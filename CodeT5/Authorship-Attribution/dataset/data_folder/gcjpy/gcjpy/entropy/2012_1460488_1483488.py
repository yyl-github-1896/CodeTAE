data = [ [int(a) for a in i.split(" ")] for i in open("C-small-attempt0.in","rU").read()[:-1].split("\n")]
 
 def recycle(number, mini, maxi):
 	number2 = str(number)
 	count = 0
 	for i in range(len(number2)):
 		number2 = number2[-1:] + number2[:-1]
 		numtemp = int(number2)
 		if (number == numtemp) or (number > numtemp):
 			continue
 		if ((numtemp <= maxi) and (numtemp > mini)):
 			#print (number,numtemp)
 			numlist.append((number,numtemp))
 			count += 1
 	return count
 # total = 0
 # for i in range(1111,2222):
 # 	total += (recycle(i,1111,2222))
 # 	print (len(set(numlist)))
 
 
 
 count = 0
 for line in data[1:]:
 	count += 1
 	total = 0
 	numlist = []
 	for a in range(line[0],(line[1])):
 		total += recycle(a,line[0], line[1])
 	print ("Case #"+str(count)+":", len(set(numlist)))