from sys import stdin
 
 def read_str(): return stdin.readline().rstrip('\n')
 def read_int(): return int(stdin.readline())
 def read_ints(): return map(int, stdin.readline().split())
 
 def read_cards():
     cards = []
     for i in range(4):
         cards.append(read_ints())
     return cards
 
 def main():
     cases = read_int()
     for case in range(1, cases + 1):
         row = read_int() - 1
         cards = read_cards()
         candidates1 = set(cards[row])
         
         row = read_int() - 1
         cards = read_cards()
         candidates2 = set(cards[row])
         
         candidates = candidates1.intersection(candidates2)
         if len(candidates) == 1:
             ans = list(candidates)[0]
         elif len(candidates) == 0:
             ans = 'Volunteer cheated!'
         else:
             ans = 'Bad magician!'
         
         print('Case #{}: {}'.format(case, ans))
         
 main()
