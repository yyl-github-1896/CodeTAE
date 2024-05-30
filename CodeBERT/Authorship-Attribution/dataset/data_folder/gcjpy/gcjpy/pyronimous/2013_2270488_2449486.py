fin = open('B-small-attempt0.in', 'r')
 fout = open('ass2.out', 'w')
 
 
 T = int(fin.readline())
 
 def check(lawn, r, c):
     h, v = True, True
     for i in range(len(lawn[0])):
         if i == c:
             continue
         if lawn[r][i] > lawn[r][c]:
             h = False
             break
     for i in range(len(lawn)):
         if i == r:
             continue
         if lawn[i][c] > lawn[r][c]:
             v = False
     return (h or v)
 
 for i in range(T):
     N, M = map(int, fin.readline().split())
     lawn = []
     for j in range(N):
         lawn.append( map(int, fin.readline().split()) )
 
     n = i + 1
     ret = True
     for j in range(len(lawn)):
         if not ret: break
         for k in range(len(lawn[0])):
             if not check(lawn, j, k):
                 ret = False
                 fout.write('Case #%i: NO\n' % n)
                 break
     if ret:
         fout.write('Case #%i: YES\n' % n)