import sys
 
 library = {'a': 'y', 'o': 'e', 'z': 'q', 'q' : 'z'}
 
 def parse_example(input, output):
     for key, value in zip(input, output):
         library[key] = value
 
 parse_example("ejp mysljylc kd kxveddknmc re jsicpdrysi", "our language is impossible to understand")
 parse_example("rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd", "there are twenty six factorial possibilities")
 parse_example("de kr kd eoya kw aej tysr re ujdr lkgc jv", "so it is okay if you want to just give up")
 
 def decode_data(input):
     output = ""
     for letter in input:
         if letter in library:
             output += library[letter]
     return output
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())
     d = {'O':0, 'B':1}
     for _t in range(t):
         s = f.readline()
         print ("Case #" + str(_t+1) + ": " + decode_data(s))
     
 
