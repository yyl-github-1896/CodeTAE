import math
 
 def ss(t, amap, bmap):
     s = 0
     for m in amap:
         if len(m) == 1 and t == m.keys()[0]:
             s += m[t]
             for b in bmap:
                 if t in b:
                     b[t] -= 1
                     if b[t] == 0:
                         b.pop(t)
             m.clear()
     return s           
 
 
 def solve(case, in_lines):
     out = 'Case #%d: '%case
  
     rn, cn = [int(x) for x in in_lines[0].split()]
     mtx = []
     for i in xrange(rn):
         mtx.append([int(x) for x in in_lines[i+1].split()])
     rmap = [{} for x in xrange(rn)]
     cmap = [{} for x in xrange(cn)]
     td = {}
     
     for i in xrange(rn):
         for j in range(cn):
             k = mtx[i][j]
             if k in rmap[i]:
                 rmap[i][k] += 1
             else:
                 rmap[i][k] = 1
             if k in cmap[j]:
                 cmap[j][k] += 1
             else:
                 cmap[j][k] = 1
             if k in td:
                 td[k] += 1
             else:
                 td[k] = 1
                 
     while len(td):
         k = min(td.keys())
         sb = ss(k, rmap, cmap)
         sb += ss(k, cmap, rmap)
         if sb == 0:
             break;
         td[k] -= sb
         if td[k] == 0:
             td.pop(k)
 
     return out + ('YES' if sb else 'NO')
 
 
 def main(raw):
     lines = raw.split('\n')
     n = int(lines[0])
     ln = 1
     outs = []
     for case in xrange(1, n+1):
         buff = []
         cl = int(lines[ln].split()[0]) + ln + 1
         while ln < cl and lines[ln]:
             buff.append(lines[ln])
             ln += 1
         s = solve(case, buff)
         print s
         outs.append(s)
     return '\n'.join(outs)
     pass
 
 if __name__ == '__main__':
     test_input = """4
 4 3
 2 5 2
 1 1 1
 2 4 2
 2 3 2
 3 3
 2 1 2
 1 1 1
 2 1 2
 5 5
 2 2 2 2 2
 2 1 1 1 2
 2 1 2 1 2
 2 1 1 1 2
 2 2 2 2 2
 1 3
 1 2 1"""
     force_no_file = False
     in_file_name = '' if force_no_file else 'B-small-attempt0.in'
     base_path = 'G:/workspace/py/codejam2013/RQ/'
     if in_file_name:
         with open(base_path + in_file_name) as f:
             raw = f.read()
     else:
         raw = test_input
     out = main(raw)
     if in_file_name:
         with open(base_path + in_file_name + '.out', 'w') as f:
             f.write(out)
     pass