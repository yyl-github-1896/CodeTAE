
 def ispal(num):
     num = str(num)
     if num == num[::-1]:
         return True
     else:
         return False
 
 def test(bot, top):
     count = []
     for i in range(bot,top+1):
         if not ((int(i**0.5)**2) == i):
             continue
         if ispal(i) and ispal(int(i**0.5)):
             count.append(i)
     return len(count)
 
 case = 1
 for line in open('C-small-attempt2.in', 'Ur'):
     if ' ' in line:
         a,b = line.split()
         res = test(int(a),int(b))
         print("Case #{0}: {1}".format(case, res))
         case += 1
 
 
