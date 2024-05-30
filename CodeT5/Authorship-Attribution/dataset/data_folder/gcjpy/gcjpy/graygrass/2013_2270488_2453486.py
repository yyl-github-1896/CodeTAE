import math
 
 mm = [0xf, 0xf0, 0xf00, 0xf000, 0x8888, 0x4444, 0x2222, 0x1111, 0x8421, 0x1248]
 
 def solve(case, in_lines):
     out = 'Case #%d: '%case
     s = ''.join(in_lines)
     x = 0
     o = 0
     nc = False
     for i in xrange(16):
         m = 1 << i
         c = s[i]
         if c == 'X':
             x |= m
         elif c == 'O':
             o |= m
         elif c == 'T':
             x |= m
             o |= m
         else:
             nc = True
     r = ''
     for m in mm:
         if m & x == m:
             r = 'X won'
             break
         if m & o == m:
             r = 'O won'
             break
     if not r:
         if nc:
             r = 'Game has not completed'
         else:
             r = 'Draw'
     
     return out + r
 
 
 def main(raw):
     lines = raw.split('\n')
     n = int(lines[0])
     ln = 0
     outs = []
     for case in xrange(1, n+1):
         buff = []
         ln += 1
         while ln < len(lines) and lines[ln]:
             buff.append(lines[ln])
             ln += 1
         s = solve(case, buff)
         print s
         outs.append(s)
     return '\n'.join(outs)
     pass
 
 if __name__ == '__main__':
     test_input = """6
 XXXT
 ....
 OO..
 ....
 
 XOXT
 XXOO
 OXOX
 XXOO
 
 XOX.
 OX..
 ....
 ....
 
 OOXX
 OXXX
 OX.T
 O..O
 
 XXXO
 ..O.
 .O..
 T...
 
 OXXX
 XO..
 ..O.
 ...O"""
     force_no_file = False
     in_file_name = '' if force_no_file else 'A-small-attempt0.in'
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