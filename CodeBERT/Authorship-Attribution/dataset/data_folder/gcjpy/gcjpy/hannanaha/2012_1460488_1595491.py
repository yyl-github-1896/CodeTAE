import math
 
 OEXT = ".out"
 IN_S = "small.in"
 IN_L = "large.in"
 CASE_PRFX = "Case #%s: "
 
 
 def avg(L):
     return 1.0*sum(L)/len(L)
 
 triplets = [[0,0,0], [0,0,1], [0,1,1], 
             [0,0,2], [0,2,2], [0,1,2],
             [10,10,9], [10,9,8], [10,9,9], [10, 10, 8],
             ]
 
 def analyze_sum(sm, tgt):
     av = 1.0 * sm / 3
     av_cls = av % 1
 
     #assume non surprising
     if av_cls > 0.1:
         ns_max_val = math.ceil(av)
     else:
         ns_max_val = av 
     
     #assume surprising
     s_max_val = 0 
     if sm >= 2 and sm <= 28:
         if av_cls > 0.5:
             s_max_val = math.ceil(av) + 1
         elif av_cls > 0.1:
             s_max_val = math.ceil(av) 
         else:
             s_max_val = av + 1
     
     if ns_max_val >= tgt:
         res = [ns_max_val, None]
         kind = 1
     elif s_max_val < tgt:
         res = [None, None]
         kind = 0
     else:
         res = [None, s_max_val]
         kind = 2
         
     print sm, tgt, av, av_cls, ns_max_val, s_max_val, res, kind
     return res, kind
 
 def analyze_triplet(trip, tgt):
     sm = sum(trip)
     analyze_triplet(sm, tgt)
     
 
 def read_input(filename):
     data = []
     with open(filename, "r") as f:
         cases = int(f.readline())
         for _ in xrange(cases):
             case = f.readline().strip().split()
             case = [int(c) for c in case]
             data.append({"ngoog": case[0], "ssurp": case[1], "ptgt": case[2],
                          "trips": case[3:]})
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
         ansys = [analyze_sum(c, case["ptgt"]) for c in case["trips"]]
         non_surp_is_enough = len([k for _, k in ansys if k == 1])
         surp_needed = len([k for _, k in ansys if k == 2])
         if surp_needed >= case["ssurp"]:
             res = non_surp_is_enough + case["ssurp"]
         else:
             res = non_surp_is_enough + surp_needed
         output.append(res)
     print "output:", output
     make_output(fname, output)
      
 
 main("examples.in")
 main("small.in")