import os, re, sys
 import unittest
 
 class Test(unittest.TestCase):
 	def test_1(self):
 		self.assertEqual(main('XXXT', '....', 'OO..', '....'), 'X won')
 	def test_2(self):
 		self.assertEqual(main('XOXT', 'XXOO', 'OXOX', 'XXOO'), 'Draw')
 	def test_3(self):
 		self.assertEqual(main('XOX.', 'OX..', '....', '....'), 'Game has not completed')
 	def test_4(self):
 		self.assertEqual(main('OOXX', 'OXXX', 'OX.T', 'O..O'), 'O won')
 	def test_5(self):
 		self.assertEqual(main('XXXO', '..O.', '.O..', 'T...'), 'O won')
 	def test_6(self):
 		self.assertEqual(main('OXXX', 'XO..', '..O.', '...O'), 'O won')
 
 #tCase = sys.stdin.readline().split()
 tCase = int(sys.stdin.readline())
 
 def main(l1, l2, l3, l4):
 	
 	resul = ganhador(l1[0], l1[1], l1[2], l1[3])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 		
 	resul = ganhador(l2[0], l2[1], l2[2], l2[3])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 		
 	resul = ganhador(l3[0], l3[1], l3[2], l3[3])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 		
 	resul = ganhador(l4[0], l4[1], l4[2], l4[3])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 		
 	# coluna
 	resul = ganhador(l1[0], l2[0], l3[0], l4[0])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 
 	resul = ganhador(l1[1], l2[1], l3[1], l4[1])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 
 	resul = ganhador(l1[2], l2[2], l3[2], l4[2])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 
 	resul = ganhador(l1[3], l2[3], l3[3], l4[3])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 
 	# /
 	resul = ganhador(l1[3], l2[2], l3[1], l4[0])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 
 	# \
 	resul = ganhador(l1[0], l2[1], l3[2], l4[3])
 	
 	if resul == 0:
 		return 'X won'
 	elif resul == 1:
 		return 'O won'
 	
 	if '.' in l1 or '.' in l2 or '.' in l3 or '.' in l4:
 		return 'Game has not completed'
 	else:
 		return 'Draw'
 	
 	
 def ganhador(a, b, c, d):
 	x = 0
 	o = 0
 	p = 0
 	if a == 'X':
 		x += 1
 		p += 1
 	if a == 'O':
 		o += 1
 		p += 1
 	if a == 'T':
 		x += 1
 		o += 1
 		p += 1
 	if b == 'X':
 		x += 1
 		p += 1
 	if b == 'O':
 		o += 1
 		p += 1
 	if b == 'T':
 		x += 1
 		o += 1
 		p += 1
 	if c == 'X':
 		x += 1
 		p += 1
 	if c == 'O':
 		o += 1
 		p += 1
 	if c == 'T':
 		x += 1
 		o += 1
 		p += 1
 	if d == 'X':
 		x += 1
 		p += 1
 	if d == 'O':
 		o += 1
 		p += 1
 	if d == 'T':
 		x += 1
 		o += 1
 		p += 1	
 	if x == 4:
 		return 0
 	elif o == 4:
 		return 1
 	elif p == 4:
 		return 2
 	else: # incompleto
 		return 3
  
 if __name__ == '__main__':
 	#unittest.main()
 	for i in xrange(tCase):	
 		l1 = [str(x) for x in sys.stdin.readline().split(' ')]
 		l2 = [str(x) for x in sys.stdin.readline().split(' ')]	
 		l3 = [str(x) for x in sys.stdin.readline().split(' ')]	
 		l4 = [str(x) for x in sys.stdin.readline().split(' ')]
 		nulo = [str(x) for x in sys.stdin.readline().split(' ')]		
 		print "Case #%d: %s" % (i + 1, main(l1[0], l2[0], l3[0], l4[0]))
 		
 		##Numbers
 		#N,M = [int(x) for x in sys.stdin.readline().split(' ')]	
 		#print "Case #%d: %d" % (i + 1, main(N,M))