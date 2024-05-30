import sys
 import string
 
 
 def won(board, mapping):
     val = int(board.translate(string.maketrans(mapping, "1100")), 2)
     for v in [0x000f, 0x00f0, 0x0f00, 0xf000,
               0x1111, 0x2222, 0x4444, 0x8888,
               0x1248, 0x8421]:
         if (val & v) == v:
             return True
     return False
 
 
 def finished(board):
     return '.' not in board
 
 
 def compute(board):
     if won(board, 'XTO.'):
         return "X won"
     if won(board, 'OTX.'):
         return "O won"
     if finished(board):
         return "Draw"
     return "Game has not completed"
 
 
 def parse():
     board = []
     for i in xrange(4):
         board.append(sys.stdin.readline().strip())
     sys.stdin.readline()
     return (''.join(board),)
 
 
 if __name__ == "__main__":
     sys.setrecursionlimit(100000)
     T = int(sys.stdin.readline().strip())
     count = 1
     part = 0
     if len(sys.argv) == 3:
         part = int(sys.argv[1])
         count = int(sys.argv[2])
     for i in xrange(T):
         data = parse()
         if i * count >= part * T and i * count < (part + 1) * T:
             result = compute(*data)
             print "Case #%d: %s" % (i + 1, result)
