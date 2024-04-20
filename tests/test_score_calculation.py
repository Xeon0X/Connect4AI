from src.score import calculateScore
from src.Game import ConnectFour
from src.Player import Player


#------------------WELCOME TO THE TEST FILE------------------
#This file is used to test the code functions.
#You can add your own tests here by looking at the examples below.
#You shoud so all the output by HAND to make sure that the code is working properly.

def test_score_calculation():
    game = ConnectFour()
    player = Player('X')

    game.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  ['X', ' ', 'X', ' ', ' ', ' ', ' '],
                  ['X', 'X', 'X', ' ', ' ', 'X', ' '],
                  ['X', 'O', 'O', 'O', ' ', 'O', ' '],
                  ['O', 'X', 'X', 'O', 'O', 'X', 'O'],
                  ['O', 'O', 'X', 'O', 'X', 'O', 'O']]

    print("Testing getDiagonals...")
    diagonals = game.getDiagonals()
    assert (len(diagonals) == 24), "getDiagonals isn't working properly (Doesn't have all the diago)"
    assert (diagonals[:12] == [['X', 'O', 'X', 'O'],
                               [' ', ' ', 'X', ' '],
                               ['X', 'X', 'O', 'O'],
                               [' ', ' ', ' ', 'O'],
                               ['X', 'O', 'O', 'X'],
                               [' ', ' ', 'O', 'O'],
                               [' ', ' ', 'X', 'O'],
                               [' ', 'X', ' ', ' '],
                               [' ', 'X', 'O', 'O'],
                               ['X', ' ', ' ', 'X'],
                               ['X', 'O', 'O', 'O'],
                               [' ', ' ', 'X', 'O']]), "getDiagonals isn't working properly (Not the right diagonals)"
    print("getDiagonals test passed!")

    print("Testing calculateScore...")
    assert (calculateScore(game, player) == -51), "calculateScore isn't working properly (Not the right value)"
    print("calculateScore test passed!")


if __name__ == "__main__":
    test_score_calculation()
