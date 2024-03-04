import math
from Game import ConnectFour
from score import calculateScore
from Player import Player

indices_order = [3, 4, 2, 5, 1, 6, 0, 7]


def custom_sort(move):
    distance_from_middle = abs(move[1] - 3.5)
    return distance_from_middle

def alphaBeta(game, max_depth, player):
    """
    This function calculates the best move for a given game state with the alphaBeta algorithm.
    """
    best_action = None
    for depth in range(1, max_depth + 1):  
        memoryBoard = {}
        eval, action = playerMax(game, depth, player, -math.inf, math.inf, memoryBoard)
        if action is not None:  
            best_action = action
        else:
            break  
    return best_action

def playerMax(game,profondeur,player,alpha,beta,memoryBoard):
    """
    This function calculates the maximum score for a given game state.
    """
    key = str(game.board)
    if key in memoryBoard:
        return memoryBoard[key], None
    
    if game.checkWin() or profondeur==0 or game.isBoardFull():
        score = calculateScore(game,player)
        memoryBoard[key] = score
        return score,None 
       
    maxEval = -math.inf
    maxAction = None
    possibleMoves = game.getPossibleMoves()
    possibleMoves.sort(key=custom_sort)
    
    for gameState, move in possibleMoves:
        eval,_ = playerMin(gameState,profondeur-1,player,alpha,beta,memoryBoard)
        if eval > maxEval:
            maxEval = eval
            maxAction = move
        alpha = max(alpha,eval)
        if beta <= alpha:
            return maxEval,maxAction
    return maxEval,maxAction



def playerMin(game,profondeur,player,alpha,beta,memoryBoard):
    """
    This function calculates the minimum score for a given game state.
    """
    key = str(game.board)
    if key in memoryBoard:
        return memoryBoard[key], None
    
    if game.checkWin() or profondeur==0 or game.isBoardFull():
        score = calculateScore(game,player)
        memoryBoard[key] = score
        return score,None 
   
    
    minEval = math.inf
    minAction = None
    possibleMoves = game.getPossibleMoves()
    possibleMoves.sort(key=custom_sort)

    for gameState, move in possibleMoves:
        eval,_ = playerMax(gameState,profondeur-1,player,alpha,beta,memoryBoard)
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
    state = False
    while True:
        game.printBoard()
        if game.isBoardFull():
            print("Draw!")
            break
        if game.currentPlayer == IA1.symbol:
            column = alphaBeta(game, 7,IA1)
            print(f"Player {IA1.symbol} played column {column}")
        else:
            column = alphaBeta(game, 7, IA2)
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
