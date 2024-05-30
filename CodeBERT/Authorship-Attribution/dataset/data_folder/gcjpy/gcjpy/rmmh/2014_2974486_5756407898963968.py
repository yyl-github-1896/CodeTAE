import sys
 if len(sys.argv) == 1:
     sys.stdin = open("A.in")
 else:
     sys.stdin = open(sys.argv[1])
 
 def to_ints(s):
     return map(int, s.split())
 
 def get_ints():
     return to_ints(raw_input())
 
 n_cases = input()
 
 for case in xrange(1, n_cases + 1):
     a_row, = get_ints()
     a_layout = [get_ints() for _ in range(4)]
     b_row, = get_ints()
     b_layout = [get_ints() for _ in range(4)]
 
     poss = set(a_layout[a_row - 1])
     poss.intersection_update(b_layout[b_row - 1])
 
     result = 'Bad magician!'
 
     if len(poss) == 0:
         result = 'Volunteer cheated!'
     elif len(poss) == 1:
         result = poss.pop()
 
     print "Case #%d: %s" % (case, result)
