#!/usr/bin/python
 
 import sys
 import re
 import math
 import string
 
 f = open(sys.argv[1],'r')
 
 num = int(f.readline())
 
 for i in range(num):
     s = f.readline().strip()
     t = s.translate(string.maketrans("yeqjpmslckdxvnribtahwfougz",
         "aozurlngeismpbtdhwyxfckjvq"))
     #print 'Case #{}:'.format(i+1), s
     print 'Case #{}:'.format(i+1), t
