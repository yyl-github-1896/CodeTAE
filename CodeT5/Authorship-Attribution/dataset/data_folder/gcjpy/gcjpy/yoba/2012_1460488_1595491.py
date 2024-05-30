def passes(p, t): #normal, surprising
     q, r = divmod(t, 3)
     if r == 0:
         return q >= p, q + 1 >= p and q
     elif r == 1:
         return q + 1 >= p, q + 1 >= p and q
     elif r == 2:
         return q + 1 >= p, q + 2 >= p
 
 for case in range(int(input())):
     st = input().strip().split()
     n, s, p, t = int(st[0]), int(st[1]), int(st[2]), list(map(int, st[3:]))
     result = 0
     for i in t:
         normal, surprising = passes(p, i)
         if normal:
             result += 1
         elif surprising and s != 0:
             result += 1
             s -= 1
     print("Case #{}: {}".format(case + 1, result))
