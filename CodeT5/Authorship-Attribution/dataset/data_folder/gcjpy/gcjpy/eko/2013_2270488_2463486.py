import os, re, sys, math
 import unittest
 
 class Test(unittest.TestCase):
 	def test_1(self):
 		self.assertEqual(main(1, 4), 2)
 	def test_2(self):
 		self.assertEqual(main(10, 120), 0)
 	def test_3(self):
 		self.assertEqual(main(100, 100000000000000), 2)
 
 #tCase = sys.stdin.readline().split()
 tCase = int(sys.stdin.readline())
 
 
 def main(M, N):
 	fns = 0
 	num = M
 	maior = math.sqrt(N)
 	int_maior = 0
 	
 	if maior.is_integer():
 		int_maior = int(maior) - 1
 		if fair(N):
 			if fair(int(maior)):
 				fns += 1
 	else:
 		int_maior = int(maior)
 		
 	while int_maior >= 1:
 		if fair(int_maior):
 			quadrado = int_maior * int_maior
 			if quadrado >= M:
 				if fair(quadrado):
 					fns += 1
 		int_maior -= 1
 	return fns
 
 def main2(M, N):
 	fns = 0
 	num = M
 	#for num in xrange(M, N + 1):
 	while num <= N:
 		result = raiz(num)
 		if result:
 			if fair(num):
 			
 				if fair(result):
 					fns += 1
 					#print num
 		#yield i
 		num += 1
 		#print raiz(num)
 	return fns
 	
 def fair(num):
 	return str(num) == str(num)[::-1]
 	#return True
 	
 def raiz(num):
 	result = math.sqrt(num)
 	#result = 1.0
 	if result.is_integer():
 		return int(result)
 	else:
 		return False
 	
 if __name__ == '__main__':
 	#unittest.main()
 	for i in xrange(tCase):	
 		#l1 = [str(x) for x in sys.stdin.readline().split(' ')]		
 		#print "Case #%d: %s" % (i + 1, main(l1[0], l2[0], l3[0], l4[0]))
 		
 		##Numbers
 		N,M = [int(x) for x in sys.stdin.readline().split(' ')]	
 		print "Case #%d: %d" % (i + 1, main(N,M))