from string import maketrans
 
 f = "abcdefghijklmnopqrstuvwxyz"
 o = "ynficwlbkuomxsevzpdrjgthaq"
         
 def partAfile(infile="C:/Users/Jeffrey/Dropbox/Google Code Jam/2011/Qualifiers/input.txt",\
               outfile="C:/Users/Jeffrey/Dropbox/Google Code Jam/2011/Qualifiers/output.txt"):
     tempF = open(infile, 'r')
     tempA = []
     for line in tempF:
         tempA.append(line.strip())
         
     N = int(tempA[0])
     
     out = open(outfile, 'w')
     for i in range(1, 1+N):
         if i != 1:
             out.write("\n")
         print "Case #" + str(i) + ": " +tempA[i].translate(maketrans(o,f))
         out.write("Case #" + str(i) + ": " +tempA[i].translate(maketrans(o,f)))
         
     
 if __name__ == "__main__":
     partAfile()
