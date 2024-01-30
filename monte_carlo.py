import curses
import math
import time
import random
from Game import ConnectFour
from minmax import checkWin


exploration = 1 / math.sqrt(2)


class Node:
    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.actions = []
        self.playedMove = move
        self.visited = 0
        self.totalReward = 0
        self.childs = []
        self.parent = parent

    def isMoveUnique(self, move):
        for child in self.childs:
            if move == child.playedMove:
                return False
        return True


def isInComputationalBudget(startTime, limit=120):
    return True if time.time() - startTime < limit else False


def backup(node, reward):
    while (node != None):
        print("While the node is not the root: ")
        node.visited += 1
        node.totalReward += reward
        reward = -reward
        print("The total reward:", node.totalReward)
        print("The next reward:", reward)
        print("Total visit: ", node.visited)
        print("On this board: ")
        node.game.printBoard()
        node = node.parent


def visualize_paths(root):
    G = nx.Graph()
    stack = [(None, root)]

    while stack:
        parent, current_node = stack.pop()
        G.add_node(current_node)
        if parent:
            G.add_edge(parent, current_node)

        for child in current_node.children:
            stack.append((current_node, child))

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.show()


def bestChild(node, exploration):
    bestChildren = []
    for child in node.childs:
        bestChildren.append([child, child.totalReward / child.visited +
                            exploration * math.sqrt((math.log(node.visited))/child.visited)])
    return max(bestChildren, key=lambda x: x[1])[0]  # get the child


def remainingMoves(node):
    possibleMoves = node.game.getPossibleMoves()
    print("\nGet all possible moves: ", possibleMoves)
    print("And remove the already played: ", node.playedMove)
    remainingMoves = [move[1] for move in possibleMoves if (
        move[1] != node.playedMove and node.isMoveUnique(move))]
    print("To get only: ", remainingMoves)
    return remainingMoves


def expand(node, remainingMoves):
    # get the column and not the temporary game state
    selectedMove = random.choice(remainingMoves)
    print("\nChoose a random one: ", selectedMove)

    child = Node(node.game.copy(), parent=node)
    child.game.makeMove(selectedMove)
    child.game.switchPlayer()
    print("The board will look like this: ")
    child.game.printBoard()
    print("Turn to ", child.game.currentPlayer)
    child.playedMove = selectedMove

    print("Create and return a child from this state")
    node.childs.append(child)
    return child


def treePolicy(node):
    print("\nIn treePolicy, check for nonterminal: ",
          node.game.isBoardFull(), checkWin(node.game))
    while not node.game.isBoardFull() and not checkWin(node.game):
        print("\nWhile non terminal:")
        moves = remainingMoves(node)
        if moves:
            print("\nIf some moves possibles: ")
            return expand(node, moves)
        else:
            print("\nNo possibles moves: ")
            node = bestChild(node, exploration)
    return node


def defaultPolicy(game):
    game = game.copy()
    finalMove = None
    while not game.isBoardFull() and not checkWin(game):
        # time.sleep(0.1)
        print("\nWhile the game is not won: ")
        move = random.choice(game.getPossibleMoves())
        print("Choose a random move:", move)
        # get the column and not the temporary game state
        game.makeMove(move[1])
        game.switchPlayer()
        print("The board looks like this after the move: ")
        game.printBoard()
        print("Turn to ", game.currentPlayer)

        finalMove = move[1]
    if finalMove != None:
        print("The game has been lose by: ", game.currentPlayer)
        game.printBoard()

        if game.isWin(finalMove) and game.currentPlayer == 'X':
            print("So punish")
            return -1
        else:
            print("So good")
            return 1
    else:
        print("Draw ?")
        game.printBoard()
        return 0


def UCTSearch(game, debug=False):
    startTime = time.time()
    node = Node(game.copy())
    while isInComputationalBudget(startTime):
        # time.sleep(0.5)
        print("\nWe are here:", node)
        node.game.printBoard()
        lastNode = treePolicy(node)
        print("\n Reward calculation")
        reward = defaultPolicy(lastNode.game)

        print("\n Backup time")
        backup(lastNode, reward)
        print("\nIn the end: ")
        lastNode.game.printBoard()

        print('\n\n\n New Iteration')
    return bestChild(node, 0).playedMove


def playMonteCarlo(game):
    while True:
        game.printBoard()

        if game.isBoardFull():
            print("Draw!")
            break
        if game.currentPlayer == 'X':
            column = UCTSearch(game)  # get column
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
