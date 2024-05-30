def solve_case(t):
     c, f, x = [float(num) for num in raw_input().strip().split()]
     current_time_usage = x / 2.0
 
     n = 1
     build_farm_time = c / (2.0 + float((n - 1) * f))
     attemp_time_usage = (x / (2.0 + float(n * f))) + build_farm_time
 
     while attemp_time_usage < current_time_usage:
         current_time_usage = attemp_time_usage
 
         n += 1
         build_farm_time += c / (2.0 + float((n - 1) * f))
         attemp_time_usage = (x / (2.0 + float(n * f))) + build_farm_time
 
     print 'Case #%d: %.7f' % (t, current_time_usage,)
 
 def main():
     t = int(raw_input().strip())
     for i in range(1, t + 1):
         solve_case(i)
 
 if __name__ == '__main__':
     main()
