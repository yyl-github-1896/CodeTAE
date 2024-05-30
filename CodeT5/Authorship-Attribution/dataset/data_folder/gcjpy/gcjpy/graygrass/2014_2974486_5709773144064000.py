import os
 import math
 
 class Solver(object):
     def __init__(self):
         pass
     
     def solve(self, inputs):
         c, f, x = [float(t) for t in inputs[0].split()]
         if x <= c:
             return '%.7f'%(x/2)
         ii = int(math.ceil((f*x-2*c)/(f*c)-1))
         if ii <= 0:
             return '%.7f'%(x/2)
         t = 0
         for i in range(ii):
             t += c/(2+i*f)
         t += x/(2+ii*f)
         return '%.7f'%t
         pass
     
     def feed(self, inputs):
         lines = [x.strip() for x in inputs]
         outputs = []
         test_case_n = int(lines[0])
         cur = 1
         for i in range(test_case_n):
             i = i
             case_line_cnt = 1
             case_inputs = lines[cur:cur+case_line_cnt]
             cur += case_line_cnt
             outputs.append(self.solve(case_inputs))
         return outputs
 
 if __name__ == '__main__':
     iname = 'B-small-attempt0.in'
 #     iname = 'foo'
     sample_in = '''
     4
 30.0 1.0 2.0
 30.0 2.0 100.0
 30.50000 3.14159 1999.19990
 500.0 4.0 2000.0
     '''
     sample_out = '''
 Case #1: 1.0000000
 Case #2: 39.1666667
 Case #3: 63.9680013
 Case #4: 526.1904762
     '''
     if os.path.exists(iname):
         with open(iname) as f:
             inputs = f.readlines()
     else:
         inputs = [x.strip() for x in sample_in.split('\n') if x.strip()]
     solver = Solver()
     outputs = solver.feed(inputs)
     fail_flag = False
     if os.path.exists(iname):
         with open(iname+'.out', 'w') as f:
             for i, v in enumerate(outputs):
                 print >> f, 'Case #%d: %s'%(i+1, str(v))
     else:
         ans = set([x.strip() for x in sample_out.split('\n') if x.strip()])
         for i, v in enumerate(outputs):
             t = 'Case #%d: %s'%(i+1, str(v))
             if t not in ans:
                 print '!!! Wrong:', t
                 fail_flag = True
     print '===================================================='
     for i, v in enumerate(outputs):
         print 'Case #%d: %s'%(i+1, str(v))
     print '===================================================='
     print 'done' if not fail_flag else 'fail'
     pass