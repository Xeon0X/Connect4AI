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
        self.reward = [] # current player p at node v

        self.children = []
        self.parent = parent


    def isMoveUnique(self, move):
        """Check if a move has already been played on an other child.

        Args:
            move (int): Column [0-6]

        Returns:
            bool: True if no other child with this move exists.
        """
        for child in self.children:
            if move == child.move:
                return False
        return True


    def bestChild(self, exploration):
        """Select the best child based on reward, visits, and exploration parameter.

        From https://www.lamsade.dauphine.fr/~cazenave/A+Survey+of+Monte+Carlo+Tree+Search+Methods.pdf : "Balance exploitation of
        the currently most promising action with exploration of alternatives which may later turn out to be superior"

        Args:
            exploration (int): _description_

        Returns:
            _type_: _description_
        """
        bestChildren = []
        for child in self.children:
            bestChildren.append([child, child.totalReward / child.visited + exploration * math.sqrt((2 * math.log(node.visited))/child.visited)])
        return max(bestChildren, key=lambda x: x[1])[0] # Returns only the child


if __name__ == "__main__":
    game = ConnectFour()
    playMonteCarlo(game)
