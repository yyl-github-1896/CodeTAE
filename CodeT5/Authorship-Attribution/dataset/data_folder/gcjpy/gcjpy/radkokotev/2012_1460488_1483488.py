from string import *
 
 def compute(A,B):
     start = A
 
     count = 0
 
     while start < B:
         temp = str(start)+str(start)[:len(str(start))-1]
         for i in range (len(str(start))):
             if int(temp[i:len(str(start))+i]) > start and int(temp[i:len(str(start))+i]) <= B:
                 count += 1
         
         start += 1
 
     return count
         
 fileName = raw_input("File name: ")
 f = open(fileName,"r")
 n = int(f.readline()[:-1])
 i=0
 for line in f:
 
     items = (line[:-1]).split()
     #items.split()
 
     A = int(items[0])
     B = int(items[1])
     print "Case #%d: %d" %(i+1,compute(A,B))
     i+=1
     
 f.close()
