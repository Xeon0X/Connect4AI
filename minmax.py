import math
from Game import ConnectFour
from score import calculateScore
from Player import Player


def minmax(game, profondeur, player):   
    """ This function calculates the best move for a given game state with the minmax algorithm.


    Args:
        game (ConnectFour): The game state.
        profondeur (int): The depth of the tree.
        player (str): The player to calculate the best move for.

    Returns:
        int: The best move for the given game state.
    """
    eval, action = playerMax(game, profondeur, player)
    return action


def playerMax(game, profondeur, player):   
    """This function calculates the maximum score for a given game state.


    Args:
        game (ConnectFour): The game state.
        profondeur (int): The depth of the tree.
        player (str): The player to calculate the best move for.

    Returns:
        int: The maximum score for the given game state.
    """
    if profondeur == 0 or game.checkWin() or game.isBoardFull():
        return calculateScore(game, player), None
    
    maxEval = -math.inf
    maxAction = None

    for gameState, move in game.getPossibleMoves():
        eval, _ = playerMin(gameState, profondeur-1, player)
        if eval > maxEval:
            maxEval = eval
            maxAction = move
    
    return maxEval, maxAction


def playerMin(game, profondeur, player):
    """ This function calculates the minimum score for a given game state.


    Args:
        game (ConnectFour): The game state.
        profondeur (int): The depth of the tree.
        player (str): The player to calculate the best move for.

    Returns:
        int: The minimum score for the given game state.
    """
    if profondeur == 0 or game.checkWin() or game.isBoardFull():
        return calculateScore(game, player), None
    
    minEval = math.inf
    minAction = None
    
    for gameState, move in game.getPossibleMoves():
        eval, _ = playerMax(gameState, profondeur-1, player)
        if eval < minEval:
            minEval = eval
            minAction = move
    
    return minEval, minAction


def playMinMax(game):
    """ This function is an example of how to use the ConnectFour class with the minmax algorithm.

    Args:
        game (ConnectFour): The game state.
    """
    IA1 = Player('X')
    IA2 = Player('O')

    while True:
        game.printBoard()

        if game.currentPlayer == IA1.symbol:
            chosenMove = minmax(game, 5, IA1)
            print(f"Player {IA1.symbol} played column {chosenMove}")
        else:
            chosenMove = minmax(game, 5, IA2)
            print(f"Player {IA2.symbol} played column {chosenMove}")
        
        if (not game.isAPossibleMove(chosenMove)):
            print("Invalid move")
            continue

        game.makeMove(chosenMove)

        if game.isWin(chosenMove):
            game.switchPlayer()
            print(f"Player {game.currentPlayer} wins!")
            game.printBoard()
            break

        if game.isBoardFull():
            print("Draw!")
            game.printBoard()
            break


if __name__ == "__main__":
    game = ConnectFour()
    playMinMax(game)