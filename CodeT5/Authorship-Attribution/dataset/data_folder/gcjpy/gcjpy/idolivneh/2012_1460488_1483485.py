import sys
 
 class Translation(object):
 	def __init__(self):
 		self.letters = {}
 		self.letters['z'] = 'q'	# from text under 'Problem'
 		self.letters['q'] = 'z'
 		self.letters[' '] = ' '
 		self.count = 0
 	
 	def update_letter(self, source, image):
 		if source in self.letters.keys():
 			if self.letters[source] != image:
 				raise Exception('old: %s-->%s. new: %s-->%s' % (source, 
 																self.letters[source],
 																source,
 																image))
 		else:
 			self.letters[source] = image
 	
 	def update_word(self, source, image):
 		for char_index, _ in enumerate(source):
 			self.update_letter(source[char_index], image[char_index])
 	
 	def update_line(self, source, image):
 		for word_index, _ in enumerate(source.strip().split(' ')):
 			self.update_word(source.strip().split(' ')[word_index],
 							 image.strip().split(' ')[word_index])
 	
 	def print_dict(self):
 		for i in xrange(ord('a'), ord('z') + 1):
 			print "%s-->%s" % (chr(i), self.letters.get(chr(i), 'None'))
 	
 	def translate_line(self, line):
 		out = ""
 		for char in line:
 			out += self.letters[char]
 		return out
 		
 def main(filepath):
 	translation = Translation()
 	before = []
 	after = []
 	with file('tounges_before.txt', 'rb') as f_before:
 		for line in f_before:
 			before.append(line)
 		
 	with file('tounges_after.txt', 'rb') as f_after:
 		for line in f_after:
 			after.append(line)
 	
 	if len(before) != len(after):
 		raise Exception('the before and after files are not of the same size')
 	
 	for line_index in xrange(len(before)):
 		translation.update_line(before[line_index], after[line_index])
 	
 	translation.print_dict()
 	
 	with file('tounges_output.txt', 'wb') as f_out:
 		with file(filepath, 'rb') as f_in:
 			for line_index, line in enumerate(f_in):
 				if line_index == 0: #T
 					continue
 				result = translation.translate_line(line.strip())
 				print
 				print line.strip()
 				print result
 				f_out.write("Case #%d: %s\n" % (line_index, result))
 			
 if __name__ == '__main__':
 	main(sys.argv[1])