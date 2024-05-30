def solve_case(t):
     interested_row = int(raw_input().strip())
     i = 1
     while i <= 4:
         row = raw_input()
         if i == interested_row:
             first_set = set(row.strip().split())
         i += 1
     interested_row = int(raw_input().strip())
     i = 1
     while i <= 4:
         row = raw_input()
         if i == interested_row:
             second_set = set(row.strip().split())
         i += 1
     ans_set = first_set & second_set
     if len(ans_set) == 1:
         print 'Case #%d: %s' % (t, ans_set.pop(),)
     elif len(ans_set) > 1:
         print 'Case #%d: Bad magician!' % (t,)
     else:
         print 'Case #%d: Volunteer cheated!' % (t,)
 
 def main():
     t = int(raw_input().strip())
     for i in range(1, t + 1):
         solve_case(i)
 
 if __name__ == '__main__':
     main()
