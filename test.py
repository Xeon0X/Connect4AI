from score import calculateScore
from Game import ConnectFour

#------------------WELCOME TO THE TEST FILE------------------
#This file is used to test the code functions.
#You can add your own tests here by looking at the examples below.
#You shoud so all the output by HAND to make sure that the code is working properly.

game = ConnectFour()

game.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
              ['X', ' ', 'X', ' ', ' ', ' ', ' '],
              ['X', 'X', 'X', ' ', ' ', 'X', ' '],
              ['X', 'O', 'O', 'O', ' ', 'O', ' '],
              ['O', 'X', 'X', 'O', 'O', 'X', 'O'],
              ['O', 'O', 'X', 'O', 'X', 'O', 'O']]


print("Testing getDiagonals...")
diagonals = game.getDiagonals()
assert (len(diagonals) == 24), "getDiagonals isn't working properly (Doesn't have all the diago)"
assert (diagonals[:12] == [['X','O','X','O'],
                                        [' ',' ','X',' '],
                                        ['X','X','O','O'],
                                        [' ',' ',' ','O'],
                                        ['X','O','O','X'],
                                        [' ',' ','O','O'],
                                        [' ',' ','X','O'],
                                        [' ','X',' ',' '],
                                        [' ','X','O','O'],
                                        ['X',' ',' ','X'],
                                        ['X','O','O','O'],
                                        [' ',' ','X','O']]), "getDiagonals isn't working properly (Not the right diagonals)"
print("Passed!")


print("Testing calculateScore...")
assert (calculateScore(game,'X') == -51), "calculateScore isn't working properly (Not the right value)"
print("Passed!")