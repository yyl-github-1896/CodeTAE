'''
 Created on Apr 14, 2012
 
 @author: moatasem
 '''
 lan={'z':'q','q':'z',' ':' '}
 
 s1=list("ejp mysljylc kd kxveddknmc re jsicpdrysi")
 e1=list ("our language is impossible to understand")
 s2=list("rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd")
 e2=list ("there are twenty six factorial possibilities")
 s3=list("de kr kd eoya kw aej tysr re ujdr lkgc jv")
 e3=list ("so it is okay if you want to just give up")
 for i in xrange(len(s1)):
     if(lan.get(s1[i])==None and s1[i]!=" "):
         lan[s1[i]]=e1[i]
     if(lan.get(s2[i])==None and s2[i]!=" "):
         lan[s2[i]]=e2[i]
     if(lan.get(s3[i])==None and s3[i]!=" "):
         lan[s3[i]]=e3[i]
         
 f = open("A-small-attempt0.in", "r")
 n=int(f.readline().strip())
 for i  in xrange(n):
     line=f.readline().strip()
     res='Case #'+str((i+1))+": "
     for j in xrange(len(line)):
         res+=str(lan.get(line[j]))
     print res
         
     
 
