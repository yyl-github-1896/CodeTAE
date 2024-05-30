"""
 num = int(raw_input('num: ').strip())
 
 c_map = [None for x in range(0, 26)]
 
 while num > 0:
 	googleres = raw_input('googleres: ').strip()
 	original = raw_input('original: ').strip()
 
 
 	ord_a = ord('a')
 	ord_z = ord('z')
 
 	i = 0
 	for c in googleres:
 		ord_c = ord(c)
 		if ord_a <= ord_c and ord_c <= ord_z:
 			c_map[ord_c - ord_a] = ord(original[i]) - ord_c
 		i += 1
 	
 	num -= 1
 
 print c_map
 """
 
 """
 c_map = [24, 6, 2, 15, 10, -3, 15, 16, -5, 11, -2, -5, -1, -12, -4, 2, 9, 2, -5, 3, -11, -6, -17, -11, -24, -9]
 i = 0
 original_list = list()
 while i < 25:
 	original_list.append(c_map[i] + i)
 	i += 1
 original_list.sort()
 print original_list
 """
 
 c_map = [24, 6, 2, 15, 10, -3, 15, 16, -5, 11, -2, -5, -1, -12, -4, 2, 9, 2, -5, 3, -11, -6, -17, -11, -24, -9]
 
 t = int(raw_input().strip())
 t_count = 1
 while t_count <= t:
 	ord_a = ord('a')
 	ord_z = ord('z')
 	googleres = raw_input().strip()
 	original = ''
 	for c in googleres:
 		ord_c = ord(c)
 		if ord_a <= ord_c and ord_c <= ord_z:
 			original += chr(c_map[ord_c - ord_a] + ord_c)
 		else:
 			original += c
 	print 'Case #%d: %s' % (t_count, original,)
 	t_count += 1
 
