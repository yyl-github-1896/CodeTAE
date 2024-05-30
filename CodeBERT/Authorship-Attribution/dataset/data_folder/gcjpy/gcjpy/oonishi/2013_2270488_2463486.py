# coding: cp932
 import sys
 f   = file(sys.argv[1])
 out = file(sys.argv[2], 'w')
 
 caseCnt = int(f.readline())
 
 Num = [
 	0,
 	1,
 	4,
 	9,
 	121,
 	484,
 	10201,
 	12321,
 	14641,
 	40804,
 	44944,
 	1002001,
 	1234321,
 	4008004,
 	100020001,
 	102030201,
 	104060401,
 	121242121,
 	123454321,
 	125686521,
 	400080004,
 	404090404,
 	10000200001,
 	10221412201,
 	12102420121,
 	12345654321,
 	40000800004,
 	1000002000001,
 	1002003002001,
 	1004006004001,
 	1020304030201,
 	1022325232201,
 	1024348434201,
 	1210024200121,
 	1212225222121,
 	1214428244121,
 	1232346432321,
 	1234567654321,
 	4000008000004,
 	4004009004004,
 ]
 
 for case in range(1, caseCnt+1):
 	L, H = f.readline().split()
 	L = int(L); H = int(H)
 	assert L <= H
 	
 	for i in range(len(Num)):
 		if L <= Num[i]:
 			break
 	else:
 		print>>out, 'Case #%d:'%case, 0
 		continue
 
 	lb = i - 1
 
 	for i in range(1, len(Num)+1):
 		if H >= Num[len(Num)-i]:
 			break
 	else:
 		print>>out, 'Case #%d:'%case, 0
 		continue
 	ub = len(Num)-i
 		
 	print>>out, 'Case #%d:'%case, ub - lb
 
 out.close()
