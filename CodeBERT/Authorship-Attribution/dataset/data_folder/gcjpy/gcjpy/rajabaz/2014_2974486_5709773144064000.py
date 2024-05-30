def time_to_get(target, num_factories, factory_cost, factory_increase):
     rate = 2.0
     t = 0
     for i in range(num_factories):
         t += factory_cost/rate
         rate += factory_increase
     return t + target/rate
     
 def solve(C,F,X):
     min_sol = None
     num_fact = 0
     while True:
         t = time_to_get(X, num_fact, C, F)
         if min_sol is None or t < min_sol:
             min_sol = t
             num_fact += 1
         else:
             return min_sol
 
 if __name__ == "__main__":
     T = int(raw_input())
     for i in range(1, T+1):
         C,F,X = map(float, raw_input().split())
         print "Case #%d: %.07f" % (i, solve(C,F,X))
