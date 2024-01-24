
import math
from Game import ConnectFour
from evaluateFunction import evaluateFunction


def checkWin(game):
    for column in range(7):
        if not game.isCollumnEmpty(column):
            if game.isWin(column):
                return True
    return False


def minmax(game, profondeur):
    eval, action = playerMax(game, profondeur)
    return action


def playerMax(game, profondeur):
    if profondeur == 0 or checkWin(game):
        return evaluateFunction(game), None
    maxEval = -math.inf
    maxAction = None
    for move, culumn in game.getPossibleMoves():
        eval, _ = playerMin(move, profondeur-1)
        if eval > maxEval:
            maxEval = eval
            maxAction = culumn
    return maxEval, maxAction


def playerMin(game, profondeur):
    if profondeur == 0 or checkWin(game):
        return evaluateFunction(game), None
    minEval = math.inf
    minAction = None
    for move, column in game.getPossibleMoves():
        eval, _ = playerMax(move, profondeur-1)
        if eval < minEval:
            minEval = eval
            minAction = column
    return minEval, minAction


def playMinMax(game):
    while True:
        game.printBoard()
        if game.isBoardFull():
            print("Draw!")
            break
        if game.currentPlayer == 'X':
            column = minmax(game, 5)
            print(f"Player {game.currentPlayer} played column {column}")
        else:
            column = int(
                input(f"Player {game.currentPlayer}, enter a column (0-6): "))
        if (not game.isAPossibleMove(column)):
            print("Invalid move")
            continue

        game.makeMove(column)
        if game.isWin(column):
            print(f"Player {game.currentPlayer} wins!")
            game.printBoard()
            break
        game.switchPlayer()


if __name__ == "__main__":
    game = ConnectFour()
    playMinMax(game)
