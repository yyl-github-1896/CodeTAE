'''
 Created on Apr 11, 2014
 
 @author: mostasem
 '''
 
 
 
 def getIntersection(A,B):
     intersect_list = []
     dict = {};
     for i in range(4):
         if(dict.get(A[i]) <> None):
             dict[A[i]] += 1
             if(intersect_list.count(A[i]) == 0):
                 intersect_list.append(A[i])
         else:
             dict[A[i]] = 1
         if(dict.get(B[i]) <> None):
             dict[B[i]] += 1
             if(intersect_list.count(B[i]) == 0):
                 intersect_list.append(B[i])
         else:
             dict[B[i]] = 1
 
     return intersect_list
 
 f_r = open('A.in',"r")
 n_test=int(f_r.readline().strip()) 
 f_w = open("A.out", "w")
 result = ""
 for i in range(n_test):
     cards1 = []
     row_index_1 = int(f_r.readline()) - 1
     for j in range(4):
         cards1.append(map(int,f_r.readline().split()))
     cards2 = []
     row_index_2 = int(f_r.readline()) - 1
     for j in range(4):
         cards2.append(map(int,f_r.readline().split())) 
 #     print cards1 
 #     print cards2
 #     print cards1[row_index_1] ,cards2[row_index_2]
     int_list =  getIntersection(cards1[row_index_1], cards2[row_index_2])
 #     print int_list
     result = ""
     if(len(int_list) == 0):
         result = "Volunteer cheated!"
     elif(len(int_list)  == 1):
         result = str(int_list[0])
     else:
         result = "Bad magician!"
     output_str='Case #{itr}: {res}'.format(itr=(i+1),res=result)
     print output_str
     f_w.write(output_str+'\n')
 f_r.close()
 f_w.close()