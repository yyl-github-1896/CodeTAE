def count_between(a, b):
 	count = 0
 	for item in range(a, b + 1):
 		rotate = len(str(item)) - 1
 		watch_list = [item,]
 		rotate_count = 0
 		item_len = len(str(item))
 		while rotate_count < rotate:
 			r_item = str(item)
 			r_item = r_item[rotate_count + 1:] + r_item[:rotate_count + 1]
 			r_item_len = len(r_item)
 			r_item = int(r_item)
 			if r_item not in watch_list and r_item > item and r_item <= b and r_item >= a and item_len == r_item_len:
 				watch_list.append(r_item)
 				count +=1
 			rotate_count += 1
 	return count
 
 pre_computed = [0, 36, 801, 12060, 161982, 2023578, 299997,]
 
 t = int(raw_input().strip())
 t_count = 1
 while t_count <= t:
 	a, b = [int(x) for x in raw_input().strip().split()]
 	#len_a = len(str(a))
 	#len_b = len(str(b))
 	#result = reduce(lambda x, y: x + y, pre_computed[len_a - 1:len_b -1], 0)
 	#print result
 	#result -= count_between(pow(10, len_a - 1), a)
 	#print result
 	#result += count_between(pow(10, len_b - 1), b)
 	#print result
 	#print 'Case #%d: %d' % (t_count, result,)
 	print 'Case #%d: %d' % (t_count, count_between(a, b),)
 	t_count += 1
 
