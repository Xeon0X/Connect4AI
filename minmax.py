import math
from Game import ConnectFour
from score import calculateScore


def checkWin(game):
    """This function checks if a player has won the game.


    Args:
        game (ConnectFour): The game to check

    Returns:
        bool: If a player has won the game or not
    """
    for column in range(7):
        if not game.isCollumnEmpty(column):
            if game.isWin(column):
                return True
    return False

  
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
    if profondeur == 0 or checkWin(game) or game.isBoardFull():
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
    if profondeur == 0 or checkWin(game) or game.isBoardFull():
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
    while True:
        game.printBoard()

        if game.currentPlayer == 'X':
            chosenMove = minmax(game, 5, game.currentPlayer)
            print(f"Player {game.currentPlayer} played column {chosenMove}")
        else:
            chosenMove = minmax(game, 5, game.currentPlayer)
            print(f"Player {game.currentPlayer} played column {chosenMove}")
        
        if (not game.isAPossibleMove(chosenMove)):
            print("Invalid move")
            continue

        game.makeMove(chosenMove)

        if game.isWin(chosenMove):
            print(f"Player {game.currentPlayer} wins!")
            game.printBoard()
            break

        if game.isBoardFull():
            print("Draw!")
            game.printBoard()
            break

        game.switchPlayer()


if __name__ == "__main__":
    game = ConnectFour()
    playMinMax(game)