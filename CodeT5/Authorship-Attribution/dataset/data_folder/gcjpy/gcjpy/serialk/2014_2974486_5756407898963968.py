T = int(input())
 
 for i in range(T):
     a1 = int(input())
     mat1 = [list(map(int, input().split())) for k in range(4)]
     a2 = int(input())
     mat2 = [list(map(int, input().split())) for k in range(4)]
     final_set = set(mat1[a1 - 1]) & set(mat2[a2 - 1])
     if not len(final_set):
         s = 'Volunteer cheated!'
     elif len(final_set) > 1:
         s = 'Bad magician!'
     else:
         s = list(final_set)[0]
     print('Case #{}: {}'.format(i + 1, s))
