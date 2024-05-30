from sys import stdin
 
 def read_ints():
     return map(int, stdin.readline().rstrip().split(' '))
 
 def is_palin(n):
     s = str(n)
     return s == s[::-1]
     
 def find(n, fas):
     for i in xrange(len(fas)):
         if fas[i] >= n:
             return i
     return len(fas)
     
 def gen_fas(max):
     fas = []
     fasappend = fas.append
     square, base, d = 1, 1, 3
     while square < max:
         if is_palin(square) and is_palin(base):
             fasappend(square)
         square += d
         d += 2
         base += 1
     return fas
     
 def main():
     MAX = 1000
     fas = gen_fas(MAX)
     
     T = int(stdin.readline())
     for Ti in xrange(T):
         A, B = read_ints()
         answer = find(B + 1, fas) - find(A, fas)
         print 'Case #{}: {}'.format(Ti + 1, answer)
         
 main()
