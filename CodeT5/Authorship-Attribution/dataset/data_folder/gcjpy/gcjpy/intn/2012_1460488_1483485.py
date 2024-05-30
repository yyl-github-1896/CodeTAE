'''
 Created on 2012-4-14
 
 @author: hemnd
 '''
 dict = {}
 strs1 = ['our language is impossible to understand', 'there are twenty six factorial possibilities', 'so it is okay if you want to just give up']
 strs0 = ['ejp mysljylc kd kxveddknmc re jsicpdrysi', 'rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd', 'de kr kd eoya kw aej tysr re ujdr lkgc jv']
 
 for i in range(3):
     for j in range(len(strs1[i])):
         c = strs0[i][j]
         if c == ' ':
             continue
         e = strs1[i][j]
         try:
             dict[c]
             print c, '=', dict[c], e
         except:
             dict[c] = e
             print c, '=', e
 
 for k in dict.keys():
     print k, dict[k]
     
 dict['q'] = 'z'
 dict['z'] = 'q'
 dict[' '] = ' '
 
 def trans(s):
     rslt = ''
     for i in range(len(s) - 1):
         rslt += dict[s[i]]
     return rslt
 
 #inputFile = open('A-small-practice.in', 'r')
 inputFile = open('A-small-attempt0.in', 'r')
 inputLines = inputFile.readlines()
 inputFile.close()
 
 N = int(inputLines[0])
 outputLines = []
 
 for i in range(1, N + 1):
     outputLines.append('Case #%d: %s\n' % (i, trans(inputLines[i])))
     print outputLines[i - 1],
 
 outputFile = open('A-small-practice.out', 'w')
 outputFile.writelines(outputLines)
 outputFile.close()
