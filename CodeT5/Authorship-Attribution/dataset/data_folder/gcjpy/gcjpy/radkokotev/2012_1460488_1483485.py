from string import *
 dictionary = {
     "a":"y",
     "b":"h",
     "c":"e",
     "d":"s",
     "e":"o",
     "f":"c",
     "g":"v",
     "h":"x",
     "i":"d",
     "j":"u",
     "k":"i",
     "l":"g",
     "m":"l",
     "n":"b",
     "o":"k",
     "p":"r",
     "q":"z",
     "r":"t",
     "s":"n",
     "t":"w",
     "u":"j",
     "v":"p",
     "w":"f",
     "x":"m",
     "y":"a",
     "z":"q",
     " ":" "    
     }
 
 def translate(sen):
     
     new_sen = ""
 
     for char in sen: #translate each charecter
         new_sen += dictionary[char]
         
     return new_sen
 
 fileName = raw_input("File name: ")
 f = open(fileName,"r")
 
 n = int(f.readline()[:-1])
 cases = [] #keeps the input msgs
 
 for i in range(n):
     cases += [f.readline()[:-1]]
 
 f.close()
 
 
 for i in range(n): # print out
     print "Case #%d: %s" %(i+1, translate(cases[i]))
     
     
 
 
     
