#! /usr/bin/env python
 #coding=utf-8
 
 def solve(icase, case_input):
     case_output = 'Case #%i: '%icase
     
     result = ""
     for c in case_input[0]:
         if c in map:
             result += map[c]
         else:
             result += c
 
     case_output += '%s'%result
     
     return case_output
 
 
 def getmap():
     inputs = ["ejp mysljylc kd kxveddknmc re jsicpdrysi",
               "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd",
               "de kr kd eoya kw aej tysr re ujdr lkgc jv"]
     outputs = ["our language is impossible to understand",
                "there are twenty six factorial possibilities",
                "so it is okay if you want to just give up"]
     map = {}
     for case in xrange(3):
         for i, c in enumerate(inputs[case]):
             map[c] = outputs[case][i]
     
     map['q'] = 'z'
     map['z'] = 'q'
     
     print map
     print len(map)
     for c in "abcdefghijklmnopqrstuvwxyz":
         if c not in map:
             print c
     return map
 
 
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
     test_data = """3
 ejp mysljylc kd kxveddknmc re jsicpdrysi
 rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
 de kr kd eoya kw aej tysr re ujdr lkgc jv
     """
     use_test_data = False
     
     map = getmap()
     
     test_file = 'A-small-attempt2.in'
     if not use_test_data and '' != test_file:
         input_file = open(test_file)
         output_file = open(test_file + '.out', 'w')
     
     main()