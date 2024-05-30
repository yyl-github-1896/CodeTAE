import copy
 import sys
 
 
 FREE = '.'
 BOMB = '*'
 CLICK = 'c'
 
 
 class Board:
 
 	def __init__(self, R, C, M):
 		self.initial_M = M
 		self.R = R
 		self.C = C
 		self.M = M
 		self.matrix = [[FREE for c in range(C)] for r in range(R)]
 		# A rectangle that says what's the current subarea we work on
 		self.endx = len(self.matrix[0])
 		self.endy = len(self.matrix)  # 0 < R * C
 		self.startx = 0
 		self.starty = 0
 
 	def fill_row(self, row):
 		for c in self.range_active_cols:
 			self.matrix[row][c] = BOMB
 		self.starty += 1
 		self.M -= self.active_cols
 
 	def fill_col(self, col):
 		for r in self.range_active_rows:
 			self.matrix[r][col] = BOMB
 		self.startx += 1
 		self.M -= self.active_rows
 
 	def pprint(self):
 		# print('startx={}, endx={}, starty={}, endy={}, M={}'
 		# 		.format(self.startx, self.endx, self.starty, self.endy, self.M))
 		for row in self.matrix:
 			for cell in row:
 				print(cell, end='')
 			print()
 
 	@property
 	def active_rows(self):
 		return self.endy - self.starty
 
 	@property
 	def active_cols(self):
 		return self.endx - self.startx
 
 	def optimize(self):
 		while 1:
 			if (self.active_cols <= self.active_rows
 					and self.active_cols <= self.M):
 				self.fill_row(self.starty)
 			elif (self.active_rows < self.active_cols
 					and self.active_rows <= self.M):
 				self.fill_col(self.startx)
 			else:
 				break
 
 	@property
 	def range_active_cols(self):
 		return range(self.startx, self.endx)
 
 	@property
 	def range_active_rows(self):
 		return range(self.starty, self.endy)
 
 	def is_free(self, row, col):
 		return self.matrix[row][col] == FREE
 
 	def place_bomb(self):
 		for row in self.range_active_rows:
 			for col in self.range_active_cols:
 				if (self.is_free(row, col) 
 						and row + 2 < self.R
 						and col + 2 < self.C):
 					self.matrix[row][col] = BOMB
 					self.M -= 1 
 					return True
 		for col in self.range_active_cols:
 			for row in self.range_active_rows:
 				if (self.is_free(row, col)
 						and row + 2 < self.R
 						and col + 2 < self.C):
 					self.matrix[row][col] = BOMB
 					self.M -= 1
 					return True
 		return False
 
 	def mark_click(self):
 		self.matrix[-1][-1] = 'c'
 
 	def win_condition(self):
 		click_row = len(self.matrix) - 1
 		click_col = len(self.matrix[0]) - 1
 		# Check the cell left of the click
 		if (click_col - 1 >= 0
 				and not self.is_free(click_row, click_col - 1)):
 			return False
 
 		if (click_row - 1 >= 0
 				and not self.is_free(click_row - 1, click_col)):
 			return False
 
 		if (click_row -1 >= 0
 				and click_col -1 >= 0
 				and not self.is_free(click_row - 1, click_col - 1)):
 			return False
 		
 		return True
 
 	def win_cond2(self):
 		if self.initial_M + 1 == self.C * self.R:
 			return True
 		return False
 
 	def solve(self):
 		self.optimize()
 		while self.M > 0 and self.place_bomb():
 			pass
 		if self.M == 0 and (self.win_condition() or self.win_cond2()):
 			self.mark_click()
 			self.pprint()
 		else:
 			print('Impossible')
 
 
 def read_case(f):
 	return map(int, f.readline().split())
 
 
 def main():
 	fn = sys.argv[1]
 	with open(fn, encoding='utf-8') as f:
 		ncases = int(f.readline())
 		for case in range(1, ncases + 1):
 			R, C, M = read_case(f)
 			print('Case #{}:'.format(case))
 			b = Board(R, C, M)
 			b.solve()
 
 
 def main1():
 	b = Board(2, 1, 1)
 	import pdb; pdb.set_trace()
 	b.solve()
 
 
 if __name__ == '__main__':
 	main()
