import math
from Game import ConnectFour
from score import calculateScore
from Player import Player


def alphaBeta(game,profondeur,player):
    """
    This function calculates the best move for a given game state with the alphaBeta algorithm.
    """
    eval,action = playerMax(game,profondeur,player, -math.inf,math.inf)
    return action

def playerMax(game,profondeur,player,alpha,beta):
    """
    This function calculates the maximum score for a given game state.
    """
    if game.checkWin() or profondeur==0 or game.isBoardFull():
        return calculateScore(game,player),None
    
    maxEval = -math.inf
    maxAction = None

    for gameState, move in game.getPossibleMoves():
        eval,_ = playerMin(gameState,profondeur-1,player,alpha,beta)
        if eval > maxEval:
            maxEval = eval
            maxAction = move
        alpha = max(alpha,eval)
        if beta <= alpha:
            return maxEval,maxAction
    return maxEval,maxAction



def playerMin(game,profondeur,player,alpha,beta):
    """
    This function calculates the minimum score for a given game state.
    """
    if game.checkWin() or profondeur==0 or game.isBoardFull():
        return calculateScore(game,player),None
    
    minEval = math.inf
    minAction = None

    for gameState, move in game.getPossibleMoves():
        eval,_ = playerMax(gameState,profondeur-1,player,alpha,beta)
        if eval < minEval:
            minEval = eval
            minAction = move
        beta = min(beta,eval)
        if beta <= alpha:
            return minEval,minAction
    return minEval,minAction


def playAlphaBeta(game):
    """ This function is an example of how to use the ConnectFour class with the alphaBeta algorithm.

    Args:
        game (ConnectFour): The game state.
    """
    IA1 = Player('X')
    IA2 = Player('O')
    while True:
        game.printBoard()
        if game.isBoardFull():
            print("Draw!")
            break
        if game.currentPlayer == IA1.symbol:
            column = alphaBeta(game, 5,IA1)
            print(f"Player {IA1.symbol} played column {column}")
        else:
            column = alphaBeta(game, 5, IA2)
            print(f"Player {IA2.symbol} played column {column}")
            #column = int(
                #input(f"Player {game.currentPlayer}, enter a column (0-6): "))
        if (not game.isAPossibleMove(column)):
            print("Invalid move")
            continue

        game.makeMove(column)
        if game.isWin(column):
            game.switchPlayer()
            print(f"Player {game.currentPlayer} wins!")
            game.printBoard()
            break


if __name__ == "__main__":
    game = ConnectFour()
    playAlphaBeta(game)
