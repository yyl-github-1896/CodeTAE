import sys
 
 
 def main():
     cases = int(sys.stdin.readline())
 
     for case in range(cases):
         row1 = int(sys.stdin.readline())
         arrangement1 = [
             map(int, sys.stdin.readline().split())
             for _ in range(4)
         ]
         chosen1 = set(arrangement1[row1 - 1])
 
         row2 = int(sys.stdin.readline())
         arrangement2 = [
             map(int, sys.stdin.readline().split())
             for _ in range(4)
         ]
         chosen2 = set(arrangement2[row2 - 1])
 
         chosen = chosen1 & chosen2
 
         if not chosen:
             print 'Case #%d: Volunteer cheated!' % (case + 1)
         elif len(chosen) != 1:
             print 'Case #%d: Bad magician!' % (case + 1)
         else:
             print 'Case #%d: %d' % (case + 1, chosen.pop())
 
 if __name__ == '__main__':
     main()
