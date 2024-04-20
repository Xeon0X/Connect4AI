import math
import time
import random

from pyvis.network import Network


class Node:
    def __init__(self, state, parent=None, action=None, visitCount=1, reward=0):
        self.state = state
        self.action = action
        self.visitCount = visitCount
        self.reward = reward
        self.children = []
        self.parent = parent

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def isActionUnique(self, action):
        """Check if a move has already been played on an other child.

        Args:
            move (int[0-6]): Column 

        Returns:
            bool: True if no other child with this move exists.
        """
        for child in self.children:
            if action == child.action:
                return False
        return True

    def remainingActions(self):
        possibleActions = self.state.getPossibleMoves()
        remainingActions = [action[1] for action in possibleActions if (
            action != self.action and self.isActionUnique(action))]
        return remainingActions

    def bestChild(self, exploration=1 / math.sqrt(2)):
        """Select the best child based on reward, visits, and exploration parameter.

        From https://www.lamsade.dauphine.fr/~cazenave/A+Survey+of+Monte+Carlo+Tree+Search+Methods.pdf : "Balance exploitation of
        the currently most promising action with exploration of alternatives which may later turn out to be superior"

        Args:
            exploration (int[0-1]): Factor influencing the balence between exploration or exploration of nodes.

        Returns:
            Node: The most promissing child according to the exploration-exploitation parameter.
        """
        bestChildren = []
        for child in self.children:
            bestChildren.append([child, child.reward / child.visitCount + exploration *
                                math.sqrt((2 * math.log(self.visitCount))/child.visitCount)])
        print(max(bestChildren, key=lambda x: x[1]))
        return max(bestChildren, key=lambda x: x[1])[0]

    def backup(self, node, reward):
        while (node != None):
            node.visitCount += 1
            node.reward += reward
            reward = -reward
            node = node.parent

    def stateTransition(self, action):
        self.state.makeMove(action)
        self.action = action
        self.state.switchPlayer()

    def expand(self, actions):
        action = random.choice(actions)
        child = Node(self.state.copy(), parent=self)
        child.stateTransition(action)
        self.addChild(child)
        return child

    def isTerminal(self):
        if (self.action is not None and self.state.isWin(self.action)) or self.state.isBoardFull():
            return True
        return False

    def treePolicy(self):
        while not self.isTerminal():
            actions = self.remainingActions()
            if actions:
                print("expand")
                return self.expand(actions)
            else:
                self = self.bestChild(exploration)

        print("last return in treePolicy")
        return self

    def getReward(self):
        if self.state.isWin(self.action):  # player agnostic
            return 1
        else:
            return 0

    def defaultPolicy(self):
        """Simulate random movements until termial state of the game and return a reward depending on win, lose, draw.

        Returns:
            int: -1 if lose, 0 if draw, 1 if win.
        """
        simulation = self.state.copy()
        while not self.isTerminal():
            action = random.choice(self.state.getPossibleMoves())[1]
            self.stateTransition(action)
        return self.getReward()

# -------------------


def isInComputationalBudget(startTime, limit=0.01):
    return True if time.time() - startTime < limit else False


def UCTSearch(game, debug=False):
    startTime = time.time()
    node = Node(game.copy())
    while isInComputationalBudget(startTime):
        printDebug(node)
        node.addChild(Node(node.state))
        print("Is in time")
        lastNode = node.treePolicy()
        print("out")
        reward = lastNode.defaultPolicy()
        lastNode.backup(lastNode, reward)
    return node.bestChild(0).action


def playMonteCarlo(game):
    while True:
        game.printBoard()
        if game.isBoardFull():
            print("Draw!")
            break
        if game.currentPlayer == 'X':
            column = UCTSearch(game, debug=True)
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


# -------------------

def createTestTree(n):
    rootNode = Node(state="Root")

    for i in range(1, n):
        child = Node(state=f"Child{i}", parent=rootNode,
                     action=f"Action{i}", reward=10, visitCount=1+i**3)
        rootNode.addChild(child)

        for j in range(1, n):
            printDebug(rootNode)
            subChild = Node(
                state=f"Child{i}.{j}", parent=child, action=f"Action{i}.{j}", visitCount=1+i * j**2)
            child.addChild(subChild)
            printDebug(rootNode)
            sub_sub_child = Node(
                state=f"Child{i}.{j}.1", parent=subChild, action=f"Action{i}.{j}.1", reward=i * j, visitCount=1+i * j**2)
            subChild.addChild(sub_sub_child)

    return rootNode


def getNormalizedRewardColor(node, maxReward):
    if maxReward != 0:
        normalizedReward = node.reward / maxReward
        hue = 120 * (1 - normalizedReward)
        color = f"hsl({hue}, 100%, 50%)"
        return color
    return f"hsl({0}, 100%, 50%)"


def getNormalizedVisitSize(node, maxVisits):
    return node.visitCount / maxVisits * 30


def calculateMaxRewardAndVisits(rootNode):
    maxReward = rootNode.reward
    maxVisits = rootNode.visitCount
    for child in rootNode.children:
        childMaxReward, childMaxVisits = calculateMaxRewardAndVisits(child)
        maxReward = max(maxReward, childMaxReward)
        maxVisits = max(maxVisits, childMaxVisits)
    return maxReward, maxVisits


def visualizeTree(rootNode):
    net = Network(notebook=True, height="950px", width="100%",
                  bgcolor="#222222", font_color="white")
    net.show_buttons()

    maxReward, maxVisits = calculateMaxRewardAndVisits(rootNode)

    def addNodesEdges(node, parentName=None):
        currentName = str(id(node))
        color = getNormalizedRewardColor(node, maxReward)
        size = getNormalizedVisitSize(node, maxVisits)
        net.add_node(
            currentName, label=f"State: {str(node.state)}\nAction: {str(node.action)}\nVisit Count: {node.visitCount}\nReward: {node.reward}", color=color, size=size)

        if parentName is not None:
            net.add_edge(parentName, currentName)

        for child in node.children:
            addNodesEdges(child, currentName)

    addNodesEdges(rootNode)

    return net


def printDebug(node, debug=True):
    if debug:
        visualizeTree(node).show("tree.html")
        input("En attente...")


root_node = createTestTree(3)
visualizeTree(root_node).show("tree.html")


# if __name__ == "__main__":
#     game = ConnectFour()
#     playMonteCarlo(game)
