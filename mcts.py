import math
import time
import random

from Game import ConnectFour

import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt


class Node:
    def __init__(self, game, parent=None, move=None, reward=0, visit=0):
        self.game = game
        self.parent = parent
        self.move = move
        self.reward = reward
        self.visit = visit
        self.children = []

    def addChild(self, childNode):
        self.children.append(childNode)


def mcts(game):
    startTime = time.time()


def isInComputationalBudget(startTime, limit=0.01):
    return True if time.time() - startTime < limit else False

# Play


def playMonteCarlo(game):
    while True:

        game.printBoard()

        if game.isBoardFull():
            print("Draw!")
            break

        if game.currentPlayer == 'X':
            column = mcts(game)
            print(f"Player {game.currentPlayer} played column {column}")
        else:
            column = int(
                input(f"Player {game.currentPlayer}, enter a column (0-6): "))
        if (not game.isAPossibleMove(column)):
            print("Invalid move")
            continue

        game.makeMove(column)

        if game.isWin(column):
            print(f"Player {game.currentPlayer} looses!")
            game.printBoard()
            break

        print(game.currentPlayer)


# Tree Management


def createRandomTree(n):
    rootNode = Node(game=ConnectFour())

    def addRandomChildren(parent, remainingNodes):
        if remainingNodes <= 0:
            return

        numChildren = random.randint(0, remainingNodes)
        for i in range(1, numChildren+1):
            childState = parent.game
            childAction = parent.move
            childReward = random.randint(0, n)
            childVisit = random.randint(0, n)

            child = Node(game=childState, parent=parent,
                         move=childAction, reward=childReward, visit=childVisit)
            parent.addChild(child)

            remainingSubNodes = remainingNodes - 1
            printDebug(rootNode, delay=0.1)
            addRandomChildren(child, remainingSubNodes)

    addRandomChildren(rootNode, n - 1)

    return rootNode


def getNormalizedRewardColor(node, maxReward):
    if maxReward != 0:
        normalizedReward = node.reward / maxReward
        hue = 120 * (1 - normalizedReward)
        color = f"hsl({hue}, 100%, 50%)"
        return color
    return f"hsl({0}, 100%, 50%)"


def getNormalizedVisitSize(node, maxVisits):
    if maxVisits != 0:
        return node.visit / maxVisits * 30
    return 1


def calculateMaxRewardAndVisits(rootNode):
    maxReward = rootNode.reward
    maxVisits = rootNode.visit
    for child in rootNode.children:
        childMaxReward, childMaxVisits = calculateMaxRewardAndVisits(child)
        maxReward = max(maxReward, childMaxReward)
        maxVisits = max(maxVisits, childMaxVisits)
    return maxReward, maxVisits


def visualizeTree(rootNode, debug=False):
    net = Network(notebook=True, height="1450px", width="100%",
                  bgcolor="#000000", font_color="white", layout={'hierarchical': {'enabled': True, 'direction': 'UD'}})
    if debug:
        net.show_buttons()

    maxReward, maxVisits = calculateMaxRewardAndVisits(rootNode)

    def addNodesEdges(node, parentName=None):
        currentName = str(id(node))
        color = getNormalizedRewardColor(node, maxReward)
        size = getNormalizedVisitSize(node, maxVisits)
        net.add_node(
            currentName, label=f"{str(node.game.currentPlayer)}, [{str(node.move)}]", color=color, size=size)

        if parentName is not None:
            net.add_edge(parentName, currentName)

        for child in node.children:
            addNodesEdges(child, currentName)

    addNodesEdges(rootNode)

    return net


def printDebug(node, delay=0):
    visualizeTree(node).show("tree.html")
    if delay == 0:
        input("Waiting input")
    else:
        time.sleep(delay)


if __name__ == "__main__":
    game = ConnectFour()
    playMonteCarlo(game)
    root_node = createRandomTree(6)
    visualizeTree(root_node).show("tree.html")
