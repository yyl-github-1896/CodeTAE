
 def checkRow(d, t):
     g = 0
     for row in d:
         a = list(row)
         a.sort()
         a = ''.join(a)
         if 'TXXX' in a or 'XXXX' in a:
             print 'Case #%i: X won' %(t/4+1)
             return 1
         if 'OOOT' in a or 'OOOO' in a:
             print 'Case #%i: O won' %(t/4+1)
             return 1
         if '.' in a:
             g = 10
     return g
 
 def checkCol(d, t):
     for j in range(4):
         col = []
         for row in d:
             col.append(row[j])
         a = list(col)
         a.sort()
         a = ''.join(a)
         if 'TXXX' in a or 'XXXX' in a:
             print 'Case #%i: X won' %(t/4+1)
             return 1
         if 'OOOT' in a or 'OOOO' in a:
             print 'Case #%i: O won' %(t/4+1)
             return 1
     return 0
 
 def checkDiag(d1, d2, t):
     a = list(d1)
     b = list(d2)
     a.sort()
     b.sort()
     a = ''.join(a)
     b = ''.join(b)
 
     if 'TXXX' in a or 'XXXX' in a:
         print 'Case #%i: X won' %(t/4+1)
         return 1
     if 'OOOT' in a or 'OOOO' in a:
         print 'Case #%i: O won' %(t/4+1)
         return 1
 
     if 'TXXX' in b or 'XXXX' in b:
         print 'Case #%i: X won' %(t/4+1)
         return 1
     if 'OOOT' in b or 'OOOO' in b:
         print 'Case #%i: O won' %(t/4+1)
         return 1
     return 0
 
 dat = raw_input()
 
 data = dat.split()
 c = int(data.pop(0))
 
 for t in range(0, 4*c, 4):
     a = checkRow(data[t:t+4],t)
     if a == 1:
         continue
     b = checkCol(data[t:t+4],t)
     if b:
         continue
     d1 = data[t][0]+data[t+1][1]+data[t+2][2]+data[t+3][3]
     d2 = data[t][3]+data[t+1][2]+data[t+2][1]+data[t+3][0]
     c = checkDiag(d1, d2,t)
     if c:
         continue
     if (a+b+c) == 0:
         print 'Case #%i: Draw' %(t/4+1)
     if a == 10:
         print 'Case #%i: Game has not completed' %(t/4+1)   
