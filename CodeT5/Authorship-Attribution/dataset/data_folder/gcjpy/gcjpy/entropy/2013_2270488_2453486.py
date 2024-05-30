
 
 infile = open('A-small-attempt0.in', 'Ur').read()[1:].split('\n\n')
 
 case = 1
 for test in infile:
     test = test.replace('\n','')
     sets = []
     if not test:
         break
 
     r = 0
     for i in range(4):
         sets.append(test[i::4])
         sets.append(test[r:r+4])
         r = r+4
     sets.append(test[0] + test[5] + test[10] + test[15])
     sets.append(test[3] + test[6] + test[9] + test[12])
 
     sets = [set(x) for x in sets]
     winner = ''
     for i in sets:
         if i.issubset({'X', 'T'}):
             winner = 'X'
             break
         if i.issubset({'O', 'T'}):
             winner = 'O'
             break
 
     if winner:
         print("Case #{0}: {1} won".format(case, winner))
     else:
         if '.' in test:
             print("Case #{0}: Game has not completed".format(case))
         else:
             print("Case #{0}: Draw".format(case))
     case += 1
 
