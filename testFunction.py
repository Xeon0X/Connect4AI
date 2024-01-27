from evaluateFunction import *
from Game import ConnectFour

game = ConnectFour()

game.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
              ['X', ' ', 'X', ' ', ' ', ' ', ' '],
              ['X', 'X', 'X', ' ', ' ', 'X', ' '],
              ['X', 'O', 'O', 'O', ' ', 'O', ' '],
              ['O', 'X', 'X', 'O', 'O', 'X', 'O'],
              ['O', 'O', 'X', 'O', 'X', 'O', 'O']]

game.switchPlayer()

print("Testing getDiagonals...")
assert (len(game.getDiagonalsUpToDown()) == 12), "getDiagonals() isn't working properly (Doesn't have all the diago)"
assert (game.getDiagonalsUpToDown() == [['X','O','X','O'],
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
                                        [' ',' ','X','O']]), "getDiagonals() isn't working properly (Not the right diagonals)"
print("Passed!")

print("Testing evaluateFunction...")
assert (evaluateFunction(game) == -51), "evaluateFunction() isn't working properly (Not the right value)"
print("Passed!")