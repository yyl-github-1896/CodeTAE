import sys
 
 from string import translate, maketrans
 
 code = maketrans("y qee"
                  "ejp mysljylc kd kxveddknmc re jsicpdrysi"
                  "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd"
                  "de kr kd eoya kw aej tysr re ujdr lkgc jv"
                  "z",
                  "a zoo"
                  "our language is impossible to understand"
                  "there are twenty six factorial possibilities"
                  "so it is okay if you want to just give up"
                  "q")
 
 if __name__ == '__main__':
     with open(sys.argv[1], 'rU') as fin, open(sys.argv[2], 'w') as fout:
         T = int(fin.readline())
         for case in xrange(1, T+1):
             line = fin.readline().strip('\n')
             decrypted = translate(line, code)
             print >> fout, "Case #{0}: {1}".format(case, decrypted)