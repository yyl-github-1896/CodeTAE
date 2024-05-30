import sys
 import Queue
 
 
 def click(C, F, X):
     states = Queue.PriorityQueue()
 
     # (time, rate, is_done)
     states.put((0.0, 2.0, False))
     while not states.empty():
         time, rate, is_done = states.get()
 
         # done
         if is_done:
             return time
 
         # two ways to move forward
         # 1. wait
         states.put((
             time + X / rate,
             rate,
             True
         ))
 
         # 2. wait for a farm
         states.put((
             time + C / rate,
             rate + F,
             False
         ))
 
     return None
 
 def main():
     cases = int(sys.stdin.readline())
 
     for case in range(cases):
         C, F, X = map(float, sys.stdin.readline().split())
         print 'Case #%d: %.7f' % (case + 1, click(C, F, X))
 
 if __name__ == '__main__':
     main()
