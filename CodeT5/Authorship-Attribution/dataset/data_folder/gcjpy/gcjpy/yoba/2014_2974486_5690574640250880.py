import itertools
 
 
 '''
 ...
 ...
 ...
 ...
 ...
 '''
 
 for i in range(int(input())):
 
     r, c, m = tuple(map(int, str.split(input())))
     count = r * c - m
     field = dict(map(lambda c: (c, "*"), itertools.product(range(c), range(r))))
     answer = "Impossible"
 
     if m == 0:
 
         answer = field
 
     elif 1 in (r, c):
 
         for p in itertools.islice(itertools.product(range(c), range(r)), count):
 
             field[p] = "."
 
         answer = field
 
     elif count in (0, 2, 3, 5, 7):
 
         pass
 
     elif count == 1:
 
         answer = field
 
     elif count // 2 < c or count == c * 2 + 1:
 
         if count % 2 != 0:
 
             tail = 3
             ncount = count - 3
 
         else:
 
             tail = 0
             ncount = count
 
         for x in range(ncount // 2):
 
             field[(x, 0)] = field[(x, 1)] = "."
 
         for x in range(tail):
 
             field[(x, 2)] = "."
 
         answer = field
 
     elif not (c == 2 and count % c == 1):
 
         for x in range(c):
 
             field[(x, 0)] = field[(x, 1)] = "."
 
         count -= 2 * c
         tail = 0
         if count % c == 1:
 
             tail = 2
             count -= 1
 
         y = 2
         while count > 0:
 
             rx = min(count, c)
             for x in range(rx):
 
                 field[(x, y)] = "."
 
             count -= rx
             y += 1
 
         for x in range(tail):
 
             field[(x, y)] = "."
 
         answer = field
 
     field[(0, 0)] = "c"
     print(str.format("Case #{}:", i + 1))
     if isinstance(answer, dict):
 
         for y in range(r):
 
             print(str.join("", map(lambda x: field[(x, y)], range(c))))
 
     else:
 
         print(answer)
