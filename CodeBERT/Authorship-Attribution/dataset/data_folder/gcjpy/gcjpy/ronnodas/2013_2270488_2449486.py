T = int(input().strip())
 
 for case in range(1,T+1):
     N,M = [int(x) for x in input().strip().split()]
     lawn = []
     for r in range(N):
         lawn.append([int(x) for x in input().strip().split()])
     rmax = [max(row) for row in lawn]
     cmax = [max(lawn[r][c] for r in range(N)) for c in range(M)]
     ans = all(lawn[r][c] == min(rmax[r],cmax[c]) for r in range(N) for c in range(M))
     ans = "YES" if ans else "NO"
     print("Case #",case,": ",ans,sep = '')
