import time
 
 OEXT = ".out"
 CASE_PRFX = "Case #%s: "
 
 MAXB = 2000000
 
 
 
 def circlify(num, cutoff=MAXB):
     numstr = str(num) + str(num)
     max_opt = len(numstr) / 2
     opts = [int(numstr[i:i+max_opt]) for i in xrange(max_opt)]
     
     # only values larger than num (also filters leading zeroes) 
     # and smaller than cutoff
     opts = [o for o in opts if o > num and o <= cutoff]
     
     #clean dupes
     return len(set(opts))
 
 def check(A, B):
     res2 = 0
     start = time.time()
     for t in xrange(A, B):
         res2 += circlify(t, B)
     print res2, time.time()-start  
 
     return res2
 
 def read_input(filename):
     data = []
     with open(filename, "r") as f:
         cases = int(f.readline())
         for _ in xrange(cases):
             case = f.readline().strip().split()
             data.append((int(case[0]), int(case[1])))
     return data
 
 def make_output(fname, output):
     fname = fname + OEXT
     with open(fname, "w") as f:
         restext = []
         for i, v in enumerate(output):
             restext.append(CASE_PRFX % (i+1,) + str(v) + "\n")
         f.writelines(restext)
     
 def main(fname):
     data = read_input(fname)
     output = []
     for case in data:
         output.append(check(case[0], case[1]))
     print "output:", output
     make_output(fname, output)
 
 main("small.in")