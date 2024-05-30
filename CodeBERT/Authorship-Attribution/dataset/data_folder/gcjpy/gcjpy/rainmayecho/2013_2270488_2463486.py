def check(a,b):
     c = 0
     n = 1
     for i in range(1,4):
         if i**2 >= a and i**2 <=b:
             c += 1
     if 44944 >= a and 44944 <= b:
         c += 1
     while n < 10:
         p1 = int('1'+'1'*n)**2
         if p1 >= a and p1 <=b:
             c += 1
         n += 1
 
 
     if 484 >= a and 484 <= b:
         c += 1
 
     n = 1
     while True:
         p2 = int('1'+'0'*n+'1')**2
         p3 = int('2'+'0'*n+'2')**2
         if p2 >= a and p2 <= b:
             c += 1
         else:
             break
         if p3 >= a and p3 <= b:
             c += 1
         else:
             continue
         n += 1
 
     n = 1
     while True:
         t = False
         for m in range(2,5):
             p4 = int('1'*m+'0'*n+'1'*m)**2
             if p4 >= a and p4 <= b:
                 c += 1
             else:
                 t = True
                 break
         if t:
             break
             
         n += 1
     return c
                 
 dat = raw_input().split()
 n = int(dat.pop(0))
 data = [int(e) for e in dat]
 
 for i in range(0, n*2, 2):
     a, b = data[i], data[i+1]
     print 'Case #%i: '%(i/2+1) + str(check(a,b)) 
 
     
