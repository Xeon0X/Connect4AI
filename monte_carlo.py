import math
import time
import random
from Game import ConnectFour
from minmax import checkWin

import curses
import time

exploration = 1 / math.sqrt(2)

class Node:
    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.actions = []
        self.playedMove = move
        self.visited = 1
        self.totalReward = 0
        self.childs = []
        self.parent = parent

    def isMoveUnique(self, move):
        for child in self.childs:
            if move == child.playedMove:
                return False
        return True


def isInComputationalBudget(startTime, limit=5):
    return True if time.time() - startTime < limit else False


def backup(node, reward):
    while (node != None):
        node.visited += 1
        node.totalReward += reward
        reward = -reward 
        node = node.parent


def bestChild(node, exploration):
    bestChildren = []
    for child in node.childs:
        bestChildren.append([child, child.totalReward / child.visited + exploration * math.sqrt((2 * math.log(node.visited))/child.visited)])
    return max(bestChildren, key=lambda x: x[1])[0] # get the child


def remainingMoves(node):
    possibleMoves = node.game.getPossibleMoves()
    remainingMoves = [move for move in possibleMoves if move != node.playedMove and node.isMoveUnique(move)]
    return remainingMoves


def expand(node):
    moves = remainingMoves(node)
    if moves:
        selectedMove = random.choice(moves) # get the column and not the temporary game state
        node.game.makeMove(selectedMove[1])
        node.game.switchPlayer()
        child = Node(node.game, parent=node)
        child.playedMove = selectedMove
        node.childs.append(child)
        return child

def treePolicy(node):
    while not node.game.isBoardFull() and not checkWin(node.game):
        if remainingMoves(node) != []:
            return expand(node)
        else:
            node = bestChild(node, exploration)
    return node

def defaultPolicy(game):
    finalMove = None
    while not checkWin(game):
        move = random.choice(game.getPossibleMoves())
        game.makeMove(move[1]) # get the column and not the temporary game state
        game.switchPlayer()
        finalMove = move[1]
    if finalMove != None :
        return 0 if game.isWin(finalMove) else 1
    else:
        return 0


def UCTSearch(game, debug=False):
    startTime = time.time()
    node = Node(game.copy())
    while isInComputationalBudget(startTime):
        lastNode = treePolicy(node)
        reward = defaultPolicy(lastNode.game)
        backup(lastNode, reward)
    return bestChild(node, 0).playedMove


def playMonteCarlo(game):
    while True:
        game.printBoard()
        if game.isBoardFull():
            print("Draw!")
            break
        if game.currentPlayer == 'X':
            column = UCTSearch(game)[1] #get column
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
    playMonteCarlo(game)
