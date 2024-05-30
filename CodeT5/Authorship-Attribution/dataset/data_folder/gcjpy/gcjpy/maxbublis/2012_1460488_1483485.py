"""
 Google Code Jam 2012 Problem A
 Usage:
     python problem_a.py < input.txt > output.txt
 """
 import sys
 
 hints = {
     'ejp mysljylc kd kxveddknmc re jsicpdrysi': 'our language is impossible to understand',
     'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd': 'there are twenty six factorial possibilities',
     'de kr kd eoya kw aej tysr re ujdr lkgc jv': 'so it is okay if you want to just give up',
 }
 
 mapping = {'q': 'z', 'z': 'q'}
 
 for k, v in hints.items():
     for from_char, to_char in zip(k, v):
         mapping[from_char] = to_char
 
 def solve_problem():
     number_of_cases = int(sys.stdin.readline())
     for i in xrange(1, number_of_cases + 1):
         case = sys.stdin.readline().strip()
         translated = ''.join(map(lambda c: mapping.get(c, c), case))
         sys.stdout.write('Case #{0}: {1}\n'.format(i, translated))
 
 if __name__ == '__main__':
     solve_problem()
