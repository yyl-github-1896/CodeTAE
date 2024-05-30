def read_case():
 
     answer = int(input())
     lines = tuple(map(lambda _: set(str.split(input())), range(4)))
     return lines[answer - 1]
 
 
 for i in range(int(input())):
 
     intersection = read_case() & read_case()
     count = len(intersection)
     if count == 1:
 
         answer = intersection.pop()
 
     elif count > 1:
 
         answer = "Bad magician!"
 
     elif count < 1:
 
         answer = "Volunteer cheated!"
 
     print(str.format("Case #{}: {}", i + 1, answer))
