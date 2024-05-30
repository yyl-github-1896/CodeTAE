#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem A. Speaking in Tongues
 # http://code.google.com/codejam/contest/1460488/dashboard#s=p0
 #
 
 import sys
 import string
 
 INPUT = '''ejp mysljylc kd kxveddknmc re jsicpdrysi
 rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
 de kr kd eoya kw aej tysr re ujdr lkgc jv'''
 OUTPUT = '''our language is impossible to understand
 there are twenty six factorial possibilities
 so it is okay if you want to just give up'''
 
 
 class Table(dict):
 	TARGET = string.ascii_lowercase
 
 	def translate(self, msg):
 		return ''.join((self[c] if c in self.TARGET else c) for c in msg)
 
 	@classmethod
 	def maketable(cls, src, dst):
 		table = cls()
 		left = set(cls.TARGET)
 		for s, d in zip(src, dst):
 			if s in table:
 				if table[s] != d:
 					raise Exception('BAD MAPPING "%s" => "%s"/"%s"' % (s, table[s], d))
 			elif s in cls.TARGET:
 				table[s] = d
 				left.remove(s)
 		if left:
 			if len(left) != 2:
 				raise Exception('left letter incorrect')
 			l1, l2 = left
 			table[l1] = l2
 			table[l2] = l1
 		return table
 
 
 def main():
 	table = Table.maketable(INPUT, OUTPUT)
 	N = int(sys.stdin.readline())
 	for index in range(N):
 		line = sys.stdin.readline().strip()
 		print 'Case #%d:' % (index + 1), table.translate(line)
 
 
 if __name__ == '__main__':
 	main()
 
