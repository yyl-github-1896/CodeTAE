
 
 INPUT = 'D-small-attempt3.in'
 OUTPUT = 'D-small-attempt3.out'
 
 
 def solve(N, naomis, kens):
     naomis.sort()
     kens.sort()
 
     def play_war(naomis, kens):
         score = 0
         for game_round in range(N):
             nweight = naomis.pop(0)
             if nweight > kens[-1]:
                 kweight = kens.pop(0)
             else:
                 for i, weight in enumerate(kens):
                     if weight > nweight:
                         kweight = kens.pop(i)
                         break
             if nweight > kweight:
                 score += 1
         return score
 
     def play_deceitful_war(naomis, kens):
         score = 0
         crap = 0
         for i, weight in enumerate(naomis):
             if weight < kens[i]:
                 crap += 1
 
         for game_round in range(N):
             if crap:
                 ntold = kens[-1] - 0.0000001
                 crap -= 1
             else:
                 ntold = naomis[-1]
             nweight = naomis.pop(0)
 
             if ntold > kens[-1]:
                 kweight = kens.pop(0)
             else:
                 for i, weight in enumerate(kens):
                     if weight > ntold:
                         kweight = kens.pop(i)
                         break
             if nweight > kweight:
                 score += 1
         return score 
 
     return play_deceitful_war(naomis[:], kens[:]), play_war(naomis[:], kens[:])
 
 
 if __name__ == '__main__':
     inp = open(INPUT)
     out = open(OUTPUT, 'w')
     
     T = int(inp.readline())
 
     for case in range(T):
         N = int(inp.readline())
         naomis = map(float, inp.readline().split())
         kens = map(float, inp.readline().split())
         sol = solve(N, naomis, kens)
         out.write('Case #%i: %i %i\n' % (case + 1, sol[0], sol[1]))