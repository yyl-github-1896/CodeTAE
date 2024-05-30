def get_number_of_test_case():
     return int(raw_input().strip())
 
 def solve_case(t):
     lines = [list(raw_input().strip()) for i in range(4)]
     raw_input()
 
     i = 0
     j = 0
 
     p_list = list()
     while i < 4:
         j = 0
         s = ''
         while j < 4:
             s += lines[i][j]
             j += 1
         p_list.append(s.replace('T', 'X'))
         p_list.append(s.replace('T', 'O'))
         i += 1
 
     j = 0
     while j < 4:
         i = 0
         s = ''
         while i < 4:
             s += lines[i][j]
             i += 1
         p_list.append(s.replace('T', 'X'))
         p_list.append(s.replace('T', 'O'))
         j += 1
     
     s = lines[0][0] + lines[1][1] + lines[2][2] + lines[3][3]
     p_list.append(s.replace('T', 'X'))
     p_list.append(s.replace('T', 'O'))
 
     s = lines[0][3] + lines[1][2] + lines[2][1] + lines[3][0]
     p_list.append(s.replace('T', 'X'))
     p_list.append(s.replace('T', 'O'))
 
     has_empty = False
     outcome = ''
     for p in p_list:
         has_empty |= '.' in p
         if p == 'XXXX':
             outcome = 'X won'
             break
         elif p == 'OOOO':
             outcome = 'O won'
             break
     if not outcome:
         if has_empty:
             outcome = 'Game has not completed'
         else:
             outcome = 'Draw'
     
     print 'Case #%d: %s' % (t, outcome,)
 
 T = get_number_of_test_case()
 t = 1
 while t <= T:
     solve_case(t)
     t += 1
 
