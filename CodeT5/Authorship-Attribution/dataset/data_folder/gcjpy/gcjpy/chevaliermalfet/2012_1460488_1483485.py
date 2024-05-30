translator = {}
 translator['a'] = 'y'
 translator['b'] = 'h'
 translator['c'] = 'e'
 translator['d'] = 's'
 translator['e'] = 'o'
 translator['f'] = 'c'
 translator['g'] = 'v'
 translator['h'] = 'x'
 translator['i'] = 'd'
 translator['j'] = 'u'
 translator['k'] = 'i'
 translator['l'] = 'g'
 translator['m'] = 'l'
 translator['n'] = 'b'
 translator['o'] = 'k'
 translator['p'] = 'r'
 translator['q'] = 'z'
 translator['r'] = 't'
 translator['s'] = 'n'
 translator['t'] = 'w'
 translator['u'] = 'j'
 translator['v'] = 'p'
 translator['w'] = 'f'
 translator['x'] = 'm'
 translator['y'] = 'a'
 translator['z'] = 'q'
 
 def translate(string, translator):
     accum = ""
     for i in range(len(string)):
         if string[i] == ' ':
             accum += ' '
         elif string[i] == '\n':
             break
         else:
             accum += translator[string[i]]
     return accum
 
 inputFile = open("A-small-attempt0.in", 'r')
 outputFile = open("tonguesOut.txt", 'w')
 numTests = int(inputFile.readline())
 
 for i in range(numTests):
     outputFile.write('Case #' + str(i+1) + ': ' + translate(inputFile.readline(), translator) + '\n')
 
 inputFile.close()
 outputFile.close()
 
