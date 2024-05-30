#
 # Google Code Jam 2012
 # Round 0: A. Speaking in Tongues
 # submission by EnTerr
 #
 
 '''
 Limits: 1 = T = 30. G contains at most 100 characters.
 None of the text is guaranteed to be valid English.
 Sample
 
 Input
 3
 ejp mysljylc kd kxveddknmc re jsicpdrysi
 rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
 de kr kd eoya kw aej tysr re ujdr lkgc jv
 
 Output
 Case #1: our language is impossible to understand
 Case #2: there are twenty six factorial possibilities
 Case #3: so it is okay if you want to just give up
 '''
 
 #import psyco
 #psyco.full()
 
 import sys
 #from time import clock
 
 inf = open(sys.argv[1])
 def input(): return inf.readline().strip()
 
 knownPairs = [
     ('zq', 'qz'),
     ('ejp mysljylc kd kxveddknmc re jsicpdrysi', 'our language is impossible to understand'),
     ('rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd', 'there are twenty six factorial possibilities'),
     ('de kr kd eoya kw aej tysr re ujdr lkgc jv', 'so it is okay if you want to just give up')
 ]
 
 xlat = [chr(0) for ch in range(256)]
 for crypt, plain in knownPairs:
     for a,b in zip(crypt, plain):
         xlat[ord(a)] = b
 for i in range(26):
     xlat[ord('A')+i] = chr(ord(xlat[ord('a')+i]) - ord('a') + ord('A'))
 xlat = ''.join(xlat)
 
 for caseNo in range(1, int(input())+1):
     #print >>sys.stderr, caseNo
     print 'Case #%d:' % caseNo, input().translate(xlat)
 
 
