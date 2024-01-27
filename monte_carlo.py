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


def isInComputationalBudget(startTime, limit=10):
    return True if time.time() - startTime < limit else False


def backup(node, reward):
    while (node != None):
        node.visited += 1
        node.totalReward += reward
        reward = -reward 
        print("\nbakcup node", node)
        print(node.childs, node.playedMove)
        print("\nbakcup node parent", node.parent)
        node = node.parent
        print("\nbakcup node 2", node)
        


def bestChild(node, exploration):
    bestChildren = []
    for child in node.childs:
        bestChildren.append([child, child.totalReward / child.visited + exploration * math.sqrt((2 * math.log(node.visited))/child.visited)])
    return max(bestChildren, key=lambda x: x[1])[0] # get the child


def remainingMoves(node):
    possibleMoves = node.game.getPossibleMoves()
    remainingMoves = [move for move in possibleMoves if move != node.playedMove and node.isMoveUnique(move)]
    print("\nremainingMoves: ", remainingMoves)
    return remainingMoves


def expand(node, remainingMoves):
    print("remaning: ", remainingMoves)
    if remainingMoves:
        print("true")
        selectedMove = random.choice(remainingMoves) # get the column and not the temporary game state
        node.game.makeMove(selectedMove[1])
        node.game.printBoard()
        node.game.switchPlayer()
        child = Node(node.game, parent=node)
        print("\nchildParent: ", child.parent)
        print("\nchild: ", child)
        child.playedMove = selectedMove
        node.childs.append(child)
        return child

def treePolicy(node):
    print(node.game.isBoardFull(), checkWin(node.game))
    node.game.printBoard()
    while not node.game.isBoardFull() and not checkWin(node.game):
        moves = remainingMoves(node)
        print("moves: ", moves)
        if moves:
            return expand(node, moves)
        else:
            node = bestChild(node, exploration)
            print("\nbestChild", node)
    print("no while ?")
    return node

def defaultPolicy(game):
    game = game.copy()
    finalMove = None
    while not checkWin(game):
        move = random.choice(game.getPossibleMoves())
        game.makeMove(move[1]) # get the column and not the temporary game state
        game.switchPlayer()
        finalMove = move[1]
    if finalMove != None :
        print("DefaultPolicy: ")
        game.printBoard()
        print(game.isWin(finalMove), game.currentPlayer)
        if game.isWin(finalMove) and game.currentPlayer == 'X':
            return 1
        else:
            return 0
    else:
        return 0


def UCTSearch(game, debug=False):
    startTime = time.time()
    node = Node(game.copy())
    while isInComputationalBudget(startTime):
        # time.sleep(1)
        print("Node", node)
        lastNode = treePolicy(node)
        reward = defaultPolicy(lastNode.game)
        backup(lastNode, reward)
        print("after backup: ", node)
        print('\n\n\n New Iteration')
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
