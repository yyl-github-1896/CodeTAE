from sys import stdin
 
 def read_str(): return stdin.readline().rstrip('\n')
 def read_int(): return int(stdin.readline())
 def read_ints(): return map(int, stdin.readline().split())
 def read_floats(): return map(float, stdin.readline().split())
 
 
 def solve_case():
     C, F, X = read_floats()
     rate = 2
     current = 0
     best = X / rate
     
     while True:
         current += C / rate
         rate += F
         next = current + X / rate
         if next < best:
             best = next
         else:
             break
     
     return best
 
     
 def main():
     cases = read_int()
     for case in range(1, cases + 1):
         print('Case #{}: {:.7f}'.format(case, solve_case()))
 
         
 main()
