for case in range(int(input())):
     a, b = tuple(map(int, input().split()))
     result = 0
     ast, bst = str(a), str(b)
     for x in range(a, b + 1):
         xst = str(x)
         added = list()
         for j in range(len(xst)):
             xstr = xst[j:] + xst[:j]
             if xstr < ast or xstr > bst:
                 continue
             elif xst < xstr and xstr not in added:
                 added.append(xstr)
                 result += 1
     print("Case #{}: {}".format(case + 1, result))
