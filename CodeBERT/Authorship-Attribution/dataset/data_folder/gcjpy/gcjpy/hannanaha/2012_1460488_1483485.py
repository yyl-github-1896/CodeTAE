import string 
 
 OEXT = ".out"
 IN_S = "small.in"
 IN_L = "large.in"
 CASE_PRFX = "Case #%s: "
 
 ddd = {}
 
 def read_input(filename):
     data = []
     with open(filename, "r") as f:
         cases = int(f.readline())
         for _ in xrange(cases):
             code = f.readline()
             data.append(code)
     return data
 
 def make_output(fname, output):
     fname = fname + OEXT
     with open(fname, "w") as f:
         restext = []
         for i, v in enumerate(output):
             restext.append(CASE_PRFX % (i+1,) + v)
         f.writelines(restext)
     
 def main(fname):
     data = read_input(fname)
     output = []
     for code in data:
         output.append("".join([ddd[k] for k in code]))
     print output
     make_output(fname, output)
     
 def mainex(fname):
     with open(fname, "r") as f:
         cases = int(f.readline())
         for _ in xrange(cases):
             code = f.readline()
             trans = f.readline()
             for i, c in enumerate(code):
                 ddd.setdefault(c, trans[i])
     
     abc = string.ascii_lowercase + " \n"
     for c in abc:
         if c not in ddd.values():
             print "not in trans:", c
             missingt = c
         if c not in ddd.keys():
             print "not in code:", c
             missingc = c
     ddd.setdefault(missingc, missingt)
     print ddd
     print len(ddd)
     return ddd
     
     
     
 mainex("examples.in")
 main("examples_raw.in")
 main("small.in")