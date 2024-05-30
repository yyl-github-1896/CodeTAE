from bisect import *
 a = [1, 4, 9, 121, 484, 10201, 12321, 14641, 40804, 44944, 1002001, 1234321, 4008004, 100020001, 102030201, 104060401, 121242121, 123454321, 125686521, 400080004, 404090404, 10000200001, 10221412201, 12102420121, 12345654321, 40000800004, 1000002000001, 1002003002001, 1004006004001, 1020304030201, 1022325232201, 1024348434201, 1210024200121, 1212225222121, 1214428244121, 1232346432321, 1234567654321, 4000008000004, 4004009004004, 100000020000001]
 A = a[:10]
 def subdfs(pre, mid, d, t, n):
     if d == t:
         k = long(''.join([pre, mid, pre[::-1]]))
         k = k * k
         if k > n:
             return [1, 0]
         sqk = str(k)
         if sqk == sqk[::-1]:
             A.append(k)
             return [0, 1]
         else:
             return [0, 0]
     res = subdfs(pre + '0', mid, d + 1, t, n)
     if res[0]: return res
     if not res[1]: return res
     res2 = subdfs(pre + '1', mid, d + 1, t, n)
     if res2[0]: return [1, res[1] + res2[1]]
     return [0, res[1] + res2[1]]
 
 def dfs(d, n):
     subdfs('1', '', 0, d, n)
     subdfs('2' + '0' * d, '', d, d, n)
     subdfs('1', '0', 0, d, n)
     subdfs('1', '1', 0, d, n)
     subdfs('1', '2', 0, d, n)
     subdfs('2' + '0' * d, '0', d, d, n)
     subdfs('2' + '0' * d, '1', d, d, n)
 
 def solve(pre):
     read_ints = lambda: map(int, raw_input().split())
     l, r = read_ints()
     cl = bisect_left(A, l)
     cr = bisect_right(A, r)
     cl_ = cr_ = 0
     for i in xrange(40):
         if a[i] < l: cl_ += 1
     for i in xrange(40):
         if a[i] <= r: cr_ += 1
     #print pre, cr_ - cl_
     print pre, cr - cl
 
 for k in xrange(1, 48):
     dfs(k, 10 ** 100 + 1)
 A.sort()
 N = int(raw_input())
 for i in xrange(1, N + 1):
     solve("Case #%d:" % i)
