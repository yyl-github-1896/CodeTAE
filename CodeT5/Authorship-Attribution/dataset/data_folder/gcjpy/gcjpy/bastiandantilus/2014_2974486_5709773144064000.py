import sys
 
 if __name__ == "__main__":
     f = sys.stdin
     if len(sys.argv) >= 2:
         fn = sys.argv[1]
         if fn != '-':
             f = open(fn)
 
     t = int(f.readline())
     for _t in range(t):
 
         C, F, X = [float(x) for x in f.readline().split()]
 
         base = X / 2.0
 
         new_strategy = old_strategy = base
         time_building = 0
         farms = 0
         fastest_speed = 2
         while new_strategy <= old_strategy:
             old_strategy = new_strategy
             time_building += C / fastest_speed
             farms += 1
             fastest_speed += F
             new_strategy = time_building + X / fastest_speed
             
         
         print ("Case #" + str(_t+1) + ": " + str(old_strategy))
     
 
