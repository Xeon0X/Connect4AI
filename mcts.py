import math
import time
import random

from Game import ConnectFour

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state # state of the game before any actions
        self.action = action # selected action to be played
        self.visitCount = 0
        self.reward = 0
        self.children = []
        self.parent = parent


import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
G.add_nodes_from(nodes)

edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12)]
G.add_edges_from(edges)

# Dessiner le graphe
pos = nx.spring_layout(G)  # disposition des nœuds
nx.draw(G, pos, with_labels=True, node_size=70, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", edge_color="gray")

# Afficher le graphe
plt.savefig('tree.png')
