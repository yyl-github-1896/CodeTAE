import sys
 
 class Triplet(object):
 	def __init__(self, i, j, k):
 		self.i = i
 		self.j = j
 		self.k = k
 		self.max_diff = max((abs(i - j), abs(i - k), abs(j - k)))
 		self.valid = self.max_diff <= 2
 		self.surprise = self.max_diff == 2
 	
 	def get_tuple(self):
 		return (self.i, self.j, self.k)
 	
 	def get_redundancies(self):
 		return [(self.i, self.j, self.k),
 				(self.i, self.k, self.j),
 				(self.j, self.i, self.k),
 				(self.j, self.k, self.i),
 				(self.k, self.i, self.j),
 				(self.k, self.j, self.i)]
 
 class Googler(object):
 	def __init__(self, total_points):
 		self.total_points = total_points
 		self.regular_triplets = []
 		self.surprise_triplets = []
 		
 		for i in xrange(0, 11):
 			if i > total_points:
 				break
 			for j in xrange(i, 11):
 				if i + j > total_points:
 					break
 				k = total_points - i - j
 				if k > 10:
 					break
 				triplet = Triplet(i, j, k)
 				self.add(triplet)
 		
 		self.can_surprise = len(self.surprise_triplets) > 0
 		self.actual_triplet = None
 		self.best_result = -1
 		
 	def add(self, triplet):
 		if not triplet.valid:
 			return
 		if triplet.surprise:
 			self.add_uniquely(triplet, is_surprise=True)
 		else:
 			self.add_uniquely(triplet, is_surprise=False)
 			
 	def add_uniquely(self, triplet, is_surprise):
 		if is_surprise:
 			input_list = self.surprise_triplets
 		else:
 			input_list = self.regular_triplets
 		for triplet_redundancy in triplet.get_redundancies():
 			if triplet_redundancy in input_list:
 				return
 		input_list.append(triplet.get_tuple())
 	
 	def __str__(self):
 		return "regular: %s\nsurprise: %s" % (self.regular_triplets,
 											  self.surprise_triplets)
 	
 	def set_googler(self, is_surprise=False):
 		if not is_surprise:
 			self.actual_triplet = self.regular_triplets[0]
 		else:
 			self.actual_triplet = self.surprise_triplets[0]
 		self.calc_best_result()
 	
 	def calc_best_result(self):
 		self.best_result = max(self.actual_triplet)
 
 		
 class Contest(object):
 	def __init__(self, num_of_googlers, results):
 		self.num = num_of_googlers
 		self.googlers = []
 		for i in xrange(self.num):
 			self.googlers.append(Googler(results[i]))
 	
 	def calc(self, num_of_surprises, p):
 		max_googlers_over_p = 0
 		for surprise_perm in self.get_permutations(num_of_surprises):
 			if not self.validate_permutation(surprise_perm):
 				continue
 			count = 0
 			for index, googler in enumerate(self.googlers):
 				googler.set_googler(index in surprise_perm)
 				if googler.best_result >= p:
 					count += 1
 			if count >= max_googlers_over_p:
 				max_googlers_over_p = count
 		return max_googlers_over_p
 	
 	def get_permutations(self, num_of_surprises):
 		results = get_perms(0, self.num, num_of_surprises)
 		if not results:
 			return [[]]
 		return results
 	
 	def validate_permutation(self, perm):
 		for googler_index in perm:
 			if not self.googlers[googler_index].can_surprise:
 				return False
 		return True
 
 def get_perms(start_index, finish_index, amount):
 	if amount == 0:
 		return []
 	result_list = []
 	for i in xrange(start_index, finish_index):
 		if amount == 1:
 			result_list.append([i])
 			continue
 		for result in get_perms(i + 1, finish_index, amount - 1):
 			new_result = [i]
 			new_result.extend(result)
 			result_list.append(new_result)
 	return result_list
 		
 def main(filepath):
 	with file('dancing_output.txt', 'wb') as f_out:
 		with file(filepath, 'rb') as f_in:
 			for line_index, line in enumerate(f_in):
 				if line_index == 0: #T
 					continue
 				input_list = line.strip().split(' ')
 				num_of_googlers = int(input_list[0])
 				num_of_surprises = int(input_list[1])
 				p = int(input_list[2])
 				results = []
 				for res in input_list[3:]:
 					results.append(int(res))
 				contest = Contest(num_of_googlers, results)
 				result = contest.calc(num_of_surprises, p)
 				
 				print
 				print line.strip()
 				print result
 				
 				f_out.write("Case #%d: %d\n" % (line_index, result))
 				
 if __name__ == '__main__':
 	main(sys.argv[1])