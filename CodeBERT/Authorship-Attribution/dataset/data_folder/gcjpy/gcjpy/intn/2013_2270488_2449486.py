'''
 Created on 13 Apr 2013
 
 @author: mengda
 '''
 expected = []
 
 def process(N, M):
     lawn = []
     for n in range(N):
         lawn.append([100] * M)
     for n in range(N):
         highest = 0
         for m in range(M):
             if expected[n][m] > highest:
                 highest = expected[n][m]
         for m in range(M):
             if lawn[n][m] > highest:
                 lawn[n][m] = highest
     for m in range(M):
         highest = 0
         for n in range(N):
             if expected[n][m] > highest:
                 highest = expected[n][m]
         for n in range(N):
             if lawn[n][m] > highest:
                 lawn[n][m] = highest
     for n in range(N):
         for m in range(M):
             if lawn[n][m] <> expected[n][m]:
                 return 'NO'
     return 'YES'
 
 f = open('B-small-attempt0.in', 'r')
 T = int(f.readline())
 outLine = []
 
 for i in range(1, T + 1):
     expected = []
     (N, M) = map(int, f.readline().split())
     for _ in range(N):
         expected.append(map(int, f.readline().split()))
     outLine.append('Case #%d: %s\n' % (i, process(N, M)))
     print outLine[-1],
 
 f.close()
 outFile = open('b.s.out', 'w')
 outFile.writelines(outLine)
 outFile.close()
