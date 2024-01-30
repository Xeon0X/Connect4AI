import math
import time
import random
from Game import ConnectFour
from minmax import checkWin


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.action = action
        self.visitCount = 0
        self.reward = 0
        self.children = []
        self.parent = parent

    def isActionUnique(self, action):
        for child in self.children:
            if action == child.action:
                return False
        return True

    def remainingActions(self):
        possibleActions = self.game.getPossibleMoves()[1]
        remainingActions = [action for action in possibleActions if (
            action != self.action and self.isActionUnique(action))]
        return remainingActions

    def bestChild(self, exploration):
        bestChildren = []
        for child in self.children:
            bestChildren.append([child, child.reward / child.visitCount + exploration *
                                math.sqrt((2 * math.log(self.visitCount))/child.visitCount)])
        return max(bestChildren, key=lambda x: x[1])[0]

    def backup(self, reward):
        while (self != None):
            self.visitCount += 1
            self.reward += reward
            self = self.parent

    def stateTransition(self, action):
        self.game.makeMove(action)
        self.action = action
        self.game.switchPlayer()

    def expand(self):
        action = random.choice(self.remainingActions())
        child = Node(self.game.copy(), parent=self)
        child.stateTransition(action)
        self.children.append(child)
        return child

    def isTerminal(self):
        if self.game.isBoardFull() or self.game.isWin(self.action):
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
