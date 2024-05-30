import unittest
 
 import sys
 
 
 
 #tCase = sys.stdin.readline().split()
 tCase = int(sys.stdin.readline())
 
 def calcTemp(taxa, X):
 	return X/taxa;
 
 def main(C, F, X):
 
 	taxa = 2.0
 	resp = 0
 	
 	
 	while True:
 		#print calcTemp(taxa, X), C/taxa + calcTemp(taxa + F, X), resp
 		if C/taxa + calcTemp(taxa + F, X) < calcTemp(taxa, X):
 			resp += C/taxa
 			taxa += F			
 		else:
 			resp += calcTemp(taxa, X)
 			return resp
 	
 	
 	return 0
 		
  
 if __name__ == '__main__':
 	#unittest.main()
 	for i in xrange(tCase):	
 		#frase = [str(x) for x in sys.stdin.readline().split(' ')]	
 		#print "Case #%d: %s" % (i + 1, main(frase[0]))
 		
 		##Numbers
 		C, F, X = [float(x) for x in sys.stdin.readline().split(' ')]
 		#print A, B, NList, BList
 		print "Case #%d: %s" % (i + 1, main(C, F, X))