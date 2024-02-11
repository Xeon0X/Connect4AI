import math
import time
import random

from Game import ConnectFour

import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt


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

    def backup(self, reward):
        while (self != None):
            self.visitCount += 1
            self.reward += reward
            reward = -reward
            self = self.parent

    def stateTransition(self, action):
        self.state.makeMove(action)
        self.action = action
        self.state.switchPlayer()

    def expand(self, actions):
        action = random.choice(actions)
        child = Node(self.state.copy(), parent=self)
        child.stateTransition(action)
        self.children.append(child)
        return child

    def isTerminal(self):
        if (self.action is not None and self.state.isWin(self.action)) or self.state.isBoardFull():
            return True
        return False

    def treePolicy(self):
        while not self.isTerminal():
            actions = self.remainingActions()
            if actions:
                return self.expand(actions)
            else:
                self = self.bestChild(exploration)
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


def isInComputationalBudget(startTime, limit=0.01):
    return True if time.time() - startTime < limit else False


def UCTSearch(game, debug=False):
    startTime = time.time()
    node = Node(game.copy())
    while isInComputationalBudget(startTime):
        lastNode = node.treePolicy()
        reward = lastNode.defaultPolicy()
        lastNode.backup(reward)
    if debug:
        visualize_tree(node).show("tree.html")
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

def createTree():
    root_node = Node(state="Root")

    for i in range(1, 20):
        child = Node(state=f"Child{i}", parent=root_node,
                     action=f"Action{i}", reward=10, visitCount=1+i**3)
        root_node.addChild(child)

        for j in range(1, 20):
            sub_child = Node(
                state=f"Child{i}.{j}", parent=child, action=f"Action{i}.{j}", visitCount=1+i * j**2)
            child.addChild(sub_child)

            sub_sub_child = Node(
                state=f"Child{i}.{j}.1", parent=sub_child, action=f"Action{i}.{j}.1", reward=i * j, visitCount=1+i * j**2)
            sub_child.addChild(sub_sub_child)

    return root_node


def get_normalized_reward_color(node, max_reward):
    normalized_reward = node.reward / max_reward
    hue = 120 * (1 - normalized_reward)
    color = f"hsl({hue}, 100%, 50%)"
    return color


def get_normalized_visit_size(node, max_visits):
    return node.visitCount / max_visits * 30


def calculate_max_reward_and_visits(root_node):
    max_reward = root_node.reward
    max_visits = root_node.visitCount
    for child in root_node.children:
        child_max_reward, child_max_visits = calculate_max_reward_and_visits(
            child)
        max_reward = max(max_reward, child_max_reward)
        max_visits = max(max_visits, child_max_visits)
    return max_reward, max_visits


def visualize_tree(root_node):
    net = Network(notebook=True, height="950px", width="100%",
                  bgcolor="#222222", font_color="white")
    net.show_buttons()

    max_reward, max_visits = calculate_max_reward_and_visits(root_node)

    def add_nodes_edges(node, parent_name=None):
        current_name = str(id(node))
        color = get_normalized_reward_color(node, max_reward)
        size = get_normalized_visit_size(node, max_visits)
        net.add_node(
            current_name, label=f"State: {str(node.state)}\nAction: {str(node.action)}\nVisit Count: {node.visitCount}\nReward: {node.reward}", color=color, size=size)

        if parent_name is not None:
            net.add_edge(parent_name, current_name)

        for child in node.children:
            add_nodes_edges(child, current_name)

    add_nodes_edges(root_node)

    return net


# root_node = createTree()
# visualize_tree(root_node).show("tree.html")

if __name__ == "__main__":
    game = ConnectFour()
    playMonteCarlo(game)
