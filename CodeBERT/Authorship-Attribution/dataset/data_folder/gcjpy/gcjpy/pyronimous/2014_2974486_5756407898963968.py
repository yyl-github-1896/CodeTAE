
 
 INPUT = 'A-small-attempt0.in'
 OUTPUT = 'A-small-attempt0.out'
 
 
 def solve(answer1, arr1, answer2, arr2):
     ret = None
 
     for card in arr1[answer1 - 1]:
         if card in arr2[answer2 - 1]:
             if ret is not None:
                 return 'Bad magician!'
             else:
                 ret = card
     if ret is None:
         return 'Volunteer cheated!'
     return ret
 
 if __name__ == '__main__':
     inp = open(INPUT)
     out = open(OUTPUT, 'w')
     
     T = int(inp.readline())
 
     def read_answer_and_arr():
         answer = int(inp.readline())
         arr = []
         for i in range(4):
             arr.append( map(int, inp.readline().split()) )
         return answer, arr
 
     for case in range(T):
         answer1, arr1 = read_answer_and_arr()
         answer2, arr2 = read_answer_and_arr()
 
         out.write('Case #%i: %s\n' % \
                         (case + 1, solve(answer1, arr1, answer2, arr2)))
