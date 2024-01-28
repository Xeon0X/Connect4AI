
import math
from Game import ConnectFour
from score import calculateScore
from minmax import checkWin


def alphaBeta(game,profondeur):
    eval,action = playerMax(game,profondeur, -math.inf,math.inf)
    return action

def playerMax(game,profondeur,alpha,beta):
    if (checkWin(game) or profondeur==0):
        return calculateScore(game),None
    
    maxEval = -math.inf
    maxAction = None

    for move, culumn in game.getPossibleMoves():
        eval,_ = playerMin(move,profondeur-1,alpha,beta)
        if eval > maxEval:
            maxEval = eval
            maxAction = culumn
        alpha = max(alpha,eval)
        if beta <= alpha:
            return maxEval,maxAction
    return maxEval,maxAction

def playerMin(game,profondeur,alpha,beta):
    if (checkWin(game) or profondeur==0):
        return calculateScore(game),None
    
    minEval = math.inf
    minAction = None

    for move, culumn in game.getPossibleMoves():
        eval,_ = playerMax(move,profondeur-1,alpha,beta)
        if eval < minEval:
            minEval = eval
            minAction = culumn
        beta = min(beta,eval)
        if beta <= alpha:
            return minEval,minAction
    return minEval,minAction


def playAlphaBeta(game):
    while True:
        game.printBoard()
        if game.isBoardFull():
            print("Draw!")
            break
        if game.currentPlayer == 'X':
            column = alphaBeta(game, 7)
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
    playAlphaBeta(game)
