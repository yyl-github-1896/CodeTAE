import sys
 
 data = [
     ['ejp mysljylc kd kxveddknmc re jsicpdrysi', 'our language is impossible to understand'],
     ['rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd', 'there are twenty six factorial possibilities'],
     ['de kr kd eoya kw aej tysr re ujdr lkgc jv', 'so it is okay if you want to just give up']]
 
 trans = {'y': 'a', 'e': 'o', 'q': 'z', 'z': 'q'}
 for row in data:
     [googlerese, english] = row
     for i in range(0, len(googlerese)):
         if not googlerese[i] in trans:
             trans[googlerese[i]] = english[i]
 
 def translate(googlerese):
     english = ''
     for c in googlerese:
         english += trans[c]
     return english
 
 T = int(sys.stdin.readline())
 for i in range(T):
     print 'Case #%s: %s' % (i+1, translate(sys.stdin.readline().strip()))
