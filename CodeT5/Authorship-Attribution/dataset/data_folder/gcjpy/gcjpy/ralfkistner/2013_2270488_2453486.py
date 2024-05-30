
 import sys
 fin = sys.stdin
 T = int(fin.readline())
 for case in range(1,T+1):
     board = []
     for i in range(4):
         row = list(fin.readline().strip())
         board.append(row)
 
     fin.readline()
 
     rows = [[], [], [], []]
     cols = [[], [], [], []]
     diags = [[], []]
 
     for i in range(4):
         for j in range(4):
             v = board[i][j]
             rows[i].append(v)
             cols[j].append(v)
             if i == j:
                 diags[0].append(v)
             if i + j == 3:
                 diags[1].append(v)
 
     buckets = rows + cols + diags
     result = 'Draw'
     filled = True
     for bucket in buckets:
         d = {'T': 0, 'X': 0, 'O': 0, '.': 0}
         for v in bucket:
             d[v] += 1
         if d['T'] + d['X'] == 4:
             result = 'X won'
             break
         if d['T'] + d['O'] == 4:
             result = 'O won'
             break
         if d['.'] > 0:
             result = 'Game has not completed'
 
     print("Case #%d: %s" % (case, result))
 
 
 
