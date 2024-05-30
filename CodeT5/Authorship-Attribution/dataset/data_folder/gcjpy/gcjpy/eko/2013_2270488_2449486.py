import os, re, sys, math
 import unittest
 from numpy import *
 
 class Test(unittest.TestCase):
 	def test_1(self):
 		self.assertEqual(main(1, 4), 2)
 	def test_2(self):
 		self.assertEqual(main(10, 120), 0)
 	def test_3(self):
 		self.assertEqual(main(100, 100000000000000), 2)
 
 tCase = int(sys.stdin.readline())
 
 
 def main(matriz, M, N):
 	#print matriz
 	
 	for i in xrange(M):
 		for j in xrange(N):
 			ana = matriz[i + 1, j + 1]
 			#print ana
 			maiores_linha = 0
 			for x in xrange(M + 2):
 				if matriz[x, j + 1] > ana:
 					maiores_linha += 1
 			
 			if maiores_linha == 0:
 				continue
 			
 			maiores_coluna = 0 
 			for y in xrange(N + 2):
 				if matriz[i + 1, y] > ana:
 					maiores_coluna += 1
 					
 			if maiores_linha >= 1 and maiores_coluna >= 1:
 				#print ana, maiores_linha, maiores_coluna
 				return 'NO'
 				
 	return 'YES'
 	
 
 
 	
 if __name__ == '__main__':
 	#unittest.main()
 	for i in xrange(tCase):	
 		##Numbers
 		N,M = [int(x) for x in sys.stdin.readline().split(' ')]
 		
 		matriz = zeros((N + 2, M + 2), dtype=int)
 		
 		for j in xrange(N + 2):
 			matriz[j][0] = 0
 			matriz[j][M + 1] = 0
 			
 		for j in xrange(M + 2):
 			matriz[0][j] = 0
 			matriz[N + 1][j] = 0
 		
 		for k in xrange(N):
 			j = 1
 			line = [str(x) for x in sys.stdin.readline().split(' ')]
 			for n in line:
 				matriz[k + 1][j] = n		
 				j += 1
 		#matriz = zeros((N + 2, M + 2), dtype=int)
 		
 		print "Case #%d: %s" % (i + 1, main(matriz, N, M))