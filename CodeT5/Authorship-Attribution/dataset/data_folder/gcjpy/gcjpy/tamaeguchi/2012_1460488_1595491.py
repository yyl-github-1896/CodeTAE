#!/usr/bin/env python
 # -*- coding:utf-8 -*-
 #
 # Problem B. Dancing With the Googlers
 # http://code.google.com/codejam/contest/1460488/dashboard#s=p1
 #
 
 import sys
 import string
 
 # 通常
 # t が 3 の倍数のとき ⇒ (t/3, t/3, t/3)
 # t が 3 の倍数 +1 のとき ⇒ (t//3 + 1, t//3, t//3)
 # t が 3 の倍数 +2 のとき ⇒ (t//3 + 1, t//3 + 1, t//3)
 
 # surprising の場合
 # t が 3 の倍数のとき ⇒ (t/3 + 1, t/3, t/3 - 1)
 # t が 3 の倍数 +1 のとき ⇒ (t//3 + 1, t//3 + 1, t//3 - 1)
 # t が 3 の倍数 +2 のとき ⇒ (t//3 + 2, t//3, t//3)
 
 
 def solve(S, p, tlist):
 	# 確実に p を超える
 	above = 0
 	# surprising で超えるかもしれない
 	consider = 0
 
 	for t in tlist:
 		avg = t / 3
 		mod = t % 3
 
 		if mod == 0:
 			# t が 3 の倍数 ⇒ (t/3, t/3, t/3)
 			if avg >= p:
 				above += 1
 			elif avg + 1 >= p and t > 0:
 				# surprising ⇒ (t/3 + 1, t/3, t/3 - 1)
 				consider += 1
 
 		elif mod == 1:
 			# t が 3 の倍数 +1 ⇒ (t//3+1, t//3, t//3)
 			if avg + 1 >= p:
 				above += 1
 			# surprising ⇒ (t//3 + 1, t//3 + 1, t//3 - 1)
 			# +1 で変わらないのでNOP
 
 		elif mod == 2:
 			# t が 3 の倍数 +2 ⇒ (t//3+1, t//3+1, t//3)
 			if avg + 1 >= p:
 				above += 1
 			elif avg + 2 >= p:
 				# surprising ⇒ (t//3 + 2, t//3, t//3)
 				consider += 1
 
 	return above + min(S, consider)
 
 
 def main(IN, OUT):
 	N = int(IN.readline())
 	for index in range(N):
 		data = map(int, IN.readline().strip().split())
 		(N, S, p), tlist = data[:3], data[3:]
 		OUT.write('Case #%d: %d\n' % (index + 1, solve(S, p, tlist)))
 
 
 if __name__ == '__main__':
 	main(sys.stdin, sys.stdout)
 
