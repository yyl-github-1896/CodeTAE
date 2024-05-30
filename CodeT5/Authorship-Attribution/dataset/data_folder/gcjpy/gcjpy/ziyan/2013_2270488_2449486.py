
 import sys
 
 def process():
     height, width = sys.stdin.readline().split()
     width = int(width)
     height = int(height)
 
     lawn = [[0 for c in range(width)] for r in range(height)]
     mark = [[0 for c in range(width)] for r in range(height)]
     settings = []
 
     for r in range(height):
         row = sys.stdin.readline().split()
         for c in range(width):
             h = int(row[c])
             lawn[r][c] = h
             if h not in settings: settings.append(h)
 
     settings = sorted(settings)
 
     for i in range(len(settings)):
         h = settings[i]
         h_next = 0
         if i < len(settings) - 1:
             h_next = settings[i + 1]
 
         # check row
         for r in range(height):
             count = 0
             for c in range(width):
                 if lawn[r][c] == h: count = count + 1
             if count == width:
                 for c in range(width): mark[r][c] = h
 
         # check col
         for c in range(width):
             count = 0
             for r in range(height):
                 if lawn[r][c] == h: count = count + 1
             if count == height:
                 for r in range(height): mark[r][c] = h
 
         # anything left?
         for c in range(width):
             for r in range(height):
                 if lawn[r][c] == h:
                     if mark[r][c] != h: return "NO"
                     lawn[r][c] = h_next
 
     return "YES"
 
         
 
 def main():
 
     count = int(sys.stdin.readline())
     for index in range(count):
         result = process()
         print "Case #%d: %s" % (index + 1, result)
 
 if __name__ == '__main__':
     main()
