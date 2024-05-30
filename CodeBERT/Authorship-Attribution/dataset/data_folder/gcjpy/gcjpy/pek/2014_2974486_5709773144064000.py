import sys
 
 lines = [line.strip() for line in open(sys.argv[1])]
 count = int(lines[0])
 
 for i in xrange(count):
     farm_cost,farm_production,target = map(float, lines[i+1].split())
     seconds = 0
     production = 2
     best = float("inf")
     while True:
         best = min(best, seconds + target / production)
         seconds += farm_cost / production
         if seconds >= best: break
         production += farm_production
 
     print "Case #%s: %.7f" % (i+1, best)
