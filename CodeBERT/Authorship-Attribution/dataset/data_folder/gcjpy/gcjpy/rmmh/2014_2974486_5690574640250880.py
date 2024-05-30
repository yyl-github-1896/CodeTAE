import sys
 if len(sys.argv) == 1:
     sys.stdin = open("C.in")
 else:
     sys.stdin = open(sys.argv[1])
 
 def to_ints(s):
     return map(int, s.split())
 
 def get_ints():
     return to_ints(raw_input())
 
 sys.setrecursionlimit(4000)
 
 def fill(rows, cols, mines):
     seen = set()
     visited = set()
 
     # we are trying to carve through a mountain 
     # and leave 'mine' squares unseen
     def search(numbered, zeros, min_numbered):
         left = (rows * cols - mines) - len(numbered)
         #print left, numbered,  min_numbered, zeros
         if left == 0:
             raise StopIteration((numbered, zeros))
         if left < 0:
             return
         for n in xrange(min_numbered, len(numbered)):
             number = numbered[n]
             if number in zeros:
                 continue
             row, col = number
             neigh = []
             if row > 0:
                 if col > 0: neigh.append((row - 1, col - 1))
                 neigh.append((row - 1, col))
                 if col < cols - 1: neigh.append((row - 1, col + 1))
             if col > 0: neigh.append((row, col - 1))
             if col < cols - 1: neigh.append((row, col + 1))
             if row < rows - 1:
                 if col > 0: neigh.append((row + 1, col - 1))
                 neigh.append((row + 1, col))
                 if col < cols - 1: neigh.append((row + 1, col + 1))
             # BUG: we might try to walk to a diagonal, oh well
             neigh = list(set(neigh) - set(numbered))
             zeros.add(number)
             search(numbered + neigh, zeros, n + 1)
             zeros.remove(number)
 
     try:
         for row in xrange(rows):
             for col in xrange(cols):
                 search([(row, col)], set(), 0)
     except StopIteration, e:
         numbered, zeros = e.message
         board = {}
         for row, col in numbered + list(zeros):
             board[row, col] = '.'
         if zeros:
             board[zeros.pop()] = 'c'
         else: # case where first click is on a number
             board[0, 0] = 'c'
         out = ''
         for row in xrange(rows):
             for col in xrange(cols):
                 out += board.get((row, col), '*')
             out += '\n'
         return out.strip()
     return 'Impossible'
 
 n_cases = input()
 for case in xrange(1, n_cases + 1):
     rows, cols, mines = get_ints()
 
     result = fill(rows, cols, mines)
 
     print "Case #%d:" % case
     print result
