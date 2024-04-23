import math
import time
import random
import numpy as np

from src.Game import ConnectFour
from src.AIs.minmax import minmax
from src.AIs.alphaBeta import alphaBeta
from src.Player import Player

from pyvis.network import Network


class Node:
    def __init__(self, game, parent=None, move=None, reward=0, visit=1):
        self.game = game
        self.parent = parent
        self.move = move
        self.reward = reward
        self.visit = visit
        self.children = []
        self.score = None

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def bestChild(self, exploration=(1 / math.sqrt(2))):
        """Select the best child based on reward, visits, and exploration parameter.

        From https://www.lamsade.dauphine.fr/~cazenave/A+Survey+of+Monte+Carlo+Tree+Search+Methods.pdf : "Balance exploitation of
        the currently most promising action with exploration of alternatives which may later turn out to be superior"

        Args:
            exploration (int[0-1]): Factor influencing the balance between exploration or exploration of nodes.

        Returns:
            Node: The most promising child according to the exploration-exploitation parameter.
        """
        bestChildren = []
        for child in self.children:
            child.score = round((child.reward / child.visit) + (exploration *
                                math.sqrt((2 * math.log(self.visit))/child.visit)), 5)
            bestChildren.append([child, child.score])

        return max(bestChildren, key=lambda x: x[1])[0]

    def expand(self, moves):
        move = random.choice(moves)
        child = Node(game=self.game.copy(), parent=self, move=move)
        child.game.makeMove(move)
        self.addChild(child)
        return child

    def remainingMoves(self):
        possibleMoves = self.game.getPossibleMoves()
        remainingMoves = [move[1]
                          for move in possibleMoves if (self.isMoveUnique(move[1]))]
        return remainingMoves

    def isMoveUnique(self, move):
        for child in self.children:
            if move == child.move:
                return False
        return True

    def isTerminal(self):  # TO CHECK
        if self.move is not None:
            if (self.game.isWin(self.move)) or self.game.isBoardFull():
                return True
        return False

    def getReward(self, depth):
        if self.game.isWin(self.move):  # player agnostic
            return (1 * 1/depth)
        else:
            return 0


def treePolicy(node, exploration=(1 / math.sqrt(2))):
    """Choose to explore a new move if still possible or continue on the most poising one

    Args:
        node (Node): The node from which the choice starts.

    Returns:
        Node: Return the chosen node, and the tree is updated.
    """
    while not node.isTerminal():
        moves = node.remainingMoves()
        if moves:
            return node.expand(moves)
        else:
            node = node.bestChild(exploration)
    return node


def defaultPolicy(node, iteration=1):
    """Simulate random movements until terminal state of the game and return a reward depending on win, lose, draw.

    Returns:
        int: -1 if lose, 0 if draw, 1 if win.
    """
    reward = []
    for i in range(iteration):
        simulation = Node(node.game.copy())
        depth = 0
        while not simulation.isTerminal():
            depth += 1
            moves = simulation.game.getPossibleMoves()
            if moves != []:
                move = random.choice(moves)[1]
                # move = alphaBeta(simulation.game, 1, Player(
                #     simulation.game.currentPlayer))
                simulation.move = move
                simulation.game.makeMove(move)
        if node.game.currentPlayer == simulation.game.currentPlayer:  # loser
            reward.append(simulation.getReward(depth))
        else:
            reward.append(-simulation.getReward(depth))  # winner

    return np.sum(reward)/len(reward)


def backup(node, reward):
    while (node != None):
        node.visit += 1
        node.reward += reward
        reward = -reward
        node = node.parent


def mcts(game, limit=10, precedent_node=None, exploration=(1 / math.sqrt(2))):
    startTime = time.time()
    iteration = 0
    if precedent_node == None:
        node = Node(game.copy())
    else:
        node = precedent_node
    while isInComputationalBudget(startTime, limit):  # and iteration <= 200:
        iteration += 1
        lastNode = treePolicy(node, exploration)
        reward = defaultPolicy(lastNode)
        backup(lastNode, reward)
        # printDebug(node, delay=0)
    # printDebug(node, delay=0)
    # print(iteration)
    return node.bestChild()


def isInComputationalBudget(startTime, limit):
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
            print(f"Player {game.currentPlayer} played column {column.move}")
        else:
            column = minmax(game, 5, game.currentPlayer)
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
            printDebug(rootNode)
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
                  bgcolor="#fafafa", font_color="black", cdn_resources='in_line')
    if debug:
        net.show_buttons()

    maxReward, maxVisits = calculateMaxRewardAndVisits(rootNode)

    def addNodesEdges(node, parentName=None):
        currentName = str(id(node))
        color = getNormalizedRewardColor(node, maxReward)
        size = getNormalizedVisitSize(node, maxVisits)
        net.add_node(
            currentName, label=f"{str(node.game.currentPlayer)}, [{str(node.move)}], \n{node.score}\n{node.reward}", color=color, size=size)

        if parentName is not None:
            net.add_edge(parentName, currentName)

        for child in node.children:
            addNodesEdges(child, currentName)

    addNodesEdges(rootNode)

    return net


def printDebug(node, delay=0.1, debug=True):
    if debug:
        visualizeTree(node, debug=True).show("tree.html")
        if delay == 0:
            input("Waiting input")
        else:
            time.sleep(delay)


if __name__ == "__main__":
    game = ConnectFour()
    playMonteCarlo(game)
    # mcts(game)
    # root_node = createRandomTree(3)
