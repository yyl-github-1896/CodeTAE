"""
 Google Code Jam 2014 Qualification Problem B
 Usage:
     python b.py < input.txt > output.txt
 """
 import sys
 
 
 def solve_problem(farm_cost, farm_rate, target):
     rate = 2.0
     farms = 0.0
 
     while (farms + target / rate) > (farms + farm_cost / rate + target / (rate + farm_rate)):
         farms = farms + farm_cost / rate
         rate = rate + farm_rate
 
     return farms + target / rate
 
 
 if __name__ == "__main__":
     num_of_cases = int(sys.stdin.readline().strip())
     for i in xrange(1, num_of_cases + 1):
         farm_cost, farm_rate, target = map(float, sys.stdin.readline().strip().split())
         print "Case #{0}: {1:9.7f}".format(i, solve_problem(farm_cost, farm_rate, target))
