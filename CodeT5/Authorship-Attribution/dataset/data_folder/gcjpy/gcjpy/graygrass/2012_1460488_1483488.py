#! /usr/bin/env python
 #coding=utf-8
 
 def solve(icase, case_input):
     case_output = 'Case #%i: '%icase
     
     result = 0
     raw = case_input[0].split()
     n = len(raw[0])
     a = int(raw[0])
     b = int(raw[1])
     
     for i in xrange(a, b):
         rslt = set()
         for t in xrange(1, n):
             tt = 10**t
             tn = 10**(n-t)
             ia, ib = divmod(i, tt)
             ii = ib*tn + ia
             if ii > i and ii <= b:
                 rslt.add(ii)
         result += len(rslt)
         
 
     case_output += '%d'%result
     
     return case_output
 
 
 def main():
     global use_test_data
     global test_data
     global input_file
     global output_file
     
     if use_test_data:
         data = [x.strip() for x in test_data.split('\n')]
     else:
         data = [x.strip() for x in input_file.readlines()]
     
     T = int(data[0])
     iLine = 1
     caseLineNum = 1
     for icase in range(1, T + 1):
         input = []
         for i in range(caseLineNum):
             input.append(data[iLine])
             iLine += 1
         rslt = solve(icase, input)
         print rslt
         if not use_test_data:
             print >> output_file, rslt
     
     if not use_test_data:
         input_file.close()
         output_file.close()
     
     
 if __name__ == '__main__':
     test_data = """5
 1 9
 10 40
 100 500
 1111 2222
 1000000 2000000
 """
     use_test_data = False
     
     test_file = 'C-small-attempt0.in'
     if not use_test_data and '' != test_file:
         input_file = open(test_file)
         output_file = open(test_file + '.out', 'w')
     
     main()