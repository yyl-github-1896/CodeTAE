import sys
 import heapq
 
 f = open( sys.argv[1] )
 f.readline()
 
 numcases = 1
 input = f.readline()
 while input != "":
 	inC,inF,inX = [float(x) for x in input.split()]
 
 	start = (0.0,0.0,2.0)
 	h = [start]
 	checked =set()
 
 	while h[0][1] < inX:
 		x = heapq.heappop(h)
 
 		if x in checked:
 			continue
 		else:
 			checked.add(x)	
 
 		time,numCookies,rate = x
 		#time to win
 		timeW = (inX - numCookies) / rate
 		heapq.heappush( h,(time+timeW,numCookies+rate*timeW,rate) )
 
 		#time to new farm
 		timeF = (inC - numCookies) / rate
 		newC = numCookies + rate*timeF
 		newT = time + timeF
 		heapq.heappush( h,(newT,(newC - inC),rate+inF) )
 		heapq.heappush( h,(newT,newC,rate) )
 		#print h
 
 	output = "{:.7f}".format(h[0][0])
 
 	print "Case #"+str(numcases)+": "+output
 	input = f.readline()
 	numcases += 1
 	