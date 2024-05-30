#!/usr/bin/python
 import sys, string
 
 #output result
 def output(case_number, status):
     print "Case #%d: %s" % (case_number, status)
 
 #solve case function
 def solve_case(board, case_number):
     has_game_completed = True
 
     # check row
     for column in range(0, 4):
         x = 0
         o = 0
         for row in range(0, 4):
             if board[column][row] == 'X':
                 x += 1
             elif board[column][row] == 'O':
                 o += 1
             elif board[column][row] == 'T':
                 x += 1
                 o += 1
             else:
                 has_game_completed = False
 
         # check if X or O won already
         if x > 3:
             output(case_number, "X won")
             return
         if o > 3:
             output(case_number, "O won")
             return
 
     # check column
     for row in range(0, 4):
         x = 0
         o = 0
         for column in range(0, 4):
             if board[column][row] == 'X':
                 x += 1
             elif board[column][row] == 'O':
                 o += 1
             elif board[column][row] == 'T':
                 x += 1
                 o += 1
 
         # check if X or O won already
         if x > 3:
             output(case_number, "X won")
             return
         if o > 3:
             output(case_number, "O won")
             return
 
     # check diagonal 1
     x = 0
     o = 0
     for rc in range(0, 4):
         if board[rc][rc] == 'X':
             x += 1
         elif board[rc][rc] == 'O':
             o += 1
         elif board[rc][rc] == 'T':
             x += 1
             o += 1
 
     # check if X or O won already
     if x > 3:
         output(case_number, "X won")
         return
     if o > 3:
         output(case_number, "O won")
         return
 
     # check diagonal 2
     x = 0
     o = 0
     for rc in range(0, 4):
         if board[rc][3 - rc] == 'X':
             x += 1
         elif board[rc][3 - rc] == 'O':
             o += 1
         elif board[rc][3 - rc] == 'T':
             x += 1
             o += 1
 
     # check if X or O won already
     if x > 3:
         output(case_number, "X won")
         return
     if o > 3:
         output(case_number, "O won")
         return
 
     if has_game_completed:
         output(case_number, "Draw")
     else:
         output(case_number, "Game has not completed")
 
 #main
 def main():
     r = sys.stdin
     if len(sys.argv) > 1:
         r = open(sys.argv[1], 'r')
 
     total_cases = r.readline()
     for case_number in range(1, int(total_cases) + 1):
         board = []
         for row in range(0, 4):
             board.append(list(r.readline().strip()))
 
         #skip the last empty line
         r.readline()
         solve_case(board, case_number)
 
 # invoke main
 if __name__ == "__main__":
     main()