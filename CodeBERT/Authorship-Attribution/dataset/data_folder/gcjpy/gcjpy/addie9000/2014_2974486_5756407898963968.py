#!/usr/bin/python
 import sys, string
 
 #solve case function
 def solve_case(answers, arrangements_of_cards, case_number):
     first_candidates = arrangements_of_cards[0][answers[0] - 1]
     second_candidates = arrangements_of_cards[1][answers[1] - 1]
     answer = set(first_candidates) & set(second_candidates)
     length_of_answer = len(answer)
     if length_of_answer > 1:
         print "Case #%d: Bad magician!" % case_number
     elif length_of_answer < 1:
         print "Case #%d: Volunteer cheated!" % case_number
     else:
         # There is only one element in the set!
         print "Case #%d: %d" % (case_number, answer.pop())
 
 #main
 r = sys.stdin
 
 if len(sys.argv) > 1:
     r = open(sys.argv[1], 'r')
 
 total_cases = r.readline()
 for case_number in range(1, int(total_cases) + 1):
     answers = []
     arrangements_of_cards = []
     answers.append(int(r.readline()))
     arrangements_of_cards.append([])
     for row in range(0, 4):
         arrangements_of_cards[0].append(map(int, r.readline().split(' ')))
     answers.append(int(r.readline()))
     arrangements_of_cards.append([])
     for row in range(0, 4):
         arrangements_of_cards[1].append(map(int, r.readline().split(' ')))
     solve_case(answers, arrangements_of_cards, case_number)
