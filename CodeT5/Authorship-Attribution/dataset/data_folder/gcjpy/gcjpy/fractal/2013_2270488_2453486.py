#! /usr/bin/python
 import re
 
 T=input()
 for i in range(1, T+1):
     game = []
     res = ""
     unfinished = False
     for j in range(4):
         game.append(raw_input())
     diag1=""
     diag2=""
     for (j, line) in zip(range(4), game):
         if re.match("(X|T){4}|(O|T){4}", line):
             res = line[0] if line[0] != 'T' else line[1]
             break
         else:
             if "." in line:
                 unfinished = True
             diag1 += line[j]
             diag2 += line[3-j]
     if not res:
         game = ["".join(x) for x in zip(*game)]
         game.append(diag1)
         game.append(diag2)
         for line in game:
             grp = re.match("(X|T){4}|(O|T){4}", line)
             if grp:
                 res = line[0] if line[0] != 'T' else line[1]
                 break
 
     if res:
         print "Case #%d: %s won" % (i, res)
     elif unfinished:
         print "Case #%d: Game has not completed" % i
     else:
         print "Case #%d: Draw" % i
     raw_input() #empty line after each test case
