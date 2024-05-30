directory = 'C:/users/hai/my projects/google code jam/2012/qualification/A/'
 
 
 t= '''ay
 bh
 ce
 ds
 eo
 fc
 gv
 hx
 id
 ju
 ki
 lg
 ml
 nb
 ok
 pr
 qz
 rt
 sn
 tw
 uj
 vp
 wf
 xm
 ya
 zq'''
 
 table = {}
 for line in t.split():
     table[line[0]] = line[1]
 
 def translate (line):
     l = list(line)
     for i in range(len(l)):
         if l[i] in table:
             l[i] = table[l[i]]
     return ''.join(l)
 
 def solve (f_in, f_out):
     T = int(f_in.readline())
     for i in range(1,T+1):
         line = f_in.readline()
         out_line = translate(line)
         f_out.write('Case #' + str(i) + ': ' + out_line)
 
 
 
 
 
 
 
 
 
 
 def main_run():
     import os
     filenames = [x for x in os.listdir (directory)]
     filenames = [x for x in filenames if x.endswith('.in')]
     l1 = [(os.stat(directory+x).st_ctime, x) for x in filenames]
     chosen_filename =  sorted(l1)[-1][1][:-3]
 
     print ('Directory : ', directory)
     print ('Chosen Filename : ',chosen_filename)
     print()
     f_in = open(directory+chosen_filename+'.in')
     f_out = open(directory+chosen_filename+'.out', 'w')
     solve(f_in,f_out)
     f_in.close()
     f_out.close()
 
 
 
 
 main_run()
