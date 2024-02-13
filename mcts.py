import math
import time
import random

from Game import ConnectFour

import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt


class Node:
    def __init__(self, state="", parent=None, action="", reward=0, visit=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.reward = reward
        self.visit = visit
        self.children = []

    def addChild(self, child_node):
        self.children.append(child_node)


def createRandomTree(n):
    rootNode = Node(state="Root")

    def addRandomChildren(parent, remainingNodes):
        if remainingNodes <= 0:
            return

        numChildren = random.randint(0, remainingNodes)
        for i in range(1, numChildren+1):
            childState = f"{parent.state}.{i}"
            childAction = f"Action{i}"
            childReward = random.randint(0, n)
            childVisit = random.randint(0, n)

            child = Node(state=childState, parent=parent,
                         action=childAction, reward=childReward, visit=childVisit)
            parent.addChild(child)

            remainingSubNodes = remainingNodes - 1
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
            currentName, label=f"State: {str(node.state)}\nAction: {str(node.action)}\nVisit Count: {node.visit}\nReward: {node.reward}", color=color, size=size)

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


root_node = createRandomTree(6)
visualizeTree(root_node).show("tree.html")
