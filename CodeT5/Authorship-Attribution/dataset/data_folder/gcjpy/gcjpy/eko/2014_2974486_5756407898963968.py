import unittest
 
 import sys
 
 
 class Test(unittest.TestCase):
 	def test_1(self):
 		self.assertEqual(main(5, 2, 2, [2,1]), 12)
 	def test_2(self):
 		self.assertEqual(main(5,2,2,[1,2]), 12)
 	def test_3(self):
 		self.assertEqual(main(3,3,4,[4,1,3,5]), 39)
 	def test_4(self):
 		self.assertEqual(main(5,2,4,[5, 1, 1, 5]), 51)
 
 
 #tCase = sys.stdin.readline().split()
 tCase = int(sys.stdin.readline())
 
 def main(A, B, AList, BList):
 	resp = 0
 	A = A - 1
 	B = B - 1
 	Alist = AList[A*4:A*4+4]
 	BList = BList[B*4:B*4+4]
 	cont = 0
 	#print Alist, BList
 	for aa in Alist:
 		if aa in BList:
 			resp = aa
 			cont += 1
 		
 	if cont == 1:
 		return resp
 	elif cont == 0:
 		return "Volunteer cheated!"
 	else:
 		return "Bad magician!"
 		
  
 if __name__ == '__main__':
 	#unittest.main()
 	for i in xrange(tCase):	
 		#frase = [str(x) for x in sys.stdin.readline().split(' ')]	
 		#print "Case #%d: %s" % (i + 1, main(frase[0]))
 		
 		##Numbers
 		A = [int(x) for x in sys.stdin.readline().split(' ')][0]
 		NList = [int(x) for x in sys.stdin.readline().split(' ')]
 		NList += [int(x) for x in sys.stdin.readline().split(' ')]
 		NList += [int(x) for x in sys.stdin.readline().split(' ')]
 		NList += [int(x) for x in sys.stdin.readline().split(' ')]
 		B = [int(x) for x in sys.stdin.readline().split(' ')][0]
 		BList = [int(x) for x in sys.stdin.readline().split(' ')]
 		BList += [int(x) for x in sys.stdin.readline().split(' ')]
 		BList += [int(x) for x in sys.stdin.readline().split(' ')]
 		BList += [int(x) for x in sys.stdin.readline().split(' ')]
 		#print A, B, NList, BList
 		print "Case #%d: %s" % (i + 1, main(A, B, NList, BList))