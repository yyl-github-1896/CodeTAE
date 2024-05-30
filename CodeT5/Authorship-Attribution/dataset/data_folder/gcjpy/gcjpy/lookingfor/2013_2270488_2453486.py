n = int(raw_input())
 
 d = {'X':2, 'O': 0, 'T':1, '.':-10}
 
 def readGame():
     return [map(lambda c:d[c], raw_input().strip()) for i in xrange(4)]
 
 def check(game):
     s = []
     for i in xrange(4): # horizontal
         s.append(sum(game[i]))
     for i in xrange(4): # vertical
         s.append(sum(map(lambda li: li[i], game)))
     d1 = d2 = 0 # diagonal
     for i in xrange(4):
         d1 += game[i][i]
         d2 += game[i][3-i]
     s.append(d1)
     s.append(d2)
     if max(s) >= 7:
         return "X won";
     gr0 = filter(lambda n: n >= 0, s)
     if len(gr0) > 0 and min(gr0) <= 1:
         return "O won"
     if min(s) < 0:
         return "Game has not completed"
     return "Draw"
 
 for i in xrange(n):
     game = readGame()
     if i + 1 < n:
         raw_input()
 
     print "Case #%d: %s" % (i+1, check(game))