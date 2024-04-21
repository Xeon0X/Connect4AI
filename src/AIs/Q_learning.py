import numpy as np
from src.Game import ConnectFour
import json
import os

def Q_learning_training(num_game = 1000000):
    Q = {}

    alpha = 0.5
    gamma = 0.95
    epsilon = 0.1

    for i in range(num_game):
        game = ConnectFour()
        state = str(game.board) + str(game.currentPlayer)

        while not game.isBoardFull():
            if np.random.uniform() < epsilon or state not in Q:
                action = np.random.choice(game.onlyPossibleMoves())
            else:
                action = max(Q[state], key=Q[state].get)

            game.makeMove(action)
            next_state = str(game.board) + str(game.currentPlayer)

            if game.isWin(action):
                Q[state][action] = 1
                break
            elif next_state not in Q:
                Q[next_state] = {}
                Q[next_state][action] = 0
            else:
                if state not in Q:
                    Q[state] = {}
                if action not in Q[state]:
                    Q[state][action] = 0
                Q[state][action] = Q[state][action] + alpha * (gamma * max(Q[next_state].values()) - Q[state][action])

            state = next_state

    with open('Q_table.json', 'w') as file:
        json.dump({str(k): {str(i): j for i, j in v.items()} for k, v in Q.items()}, file)


class QLearning:
    def __init__(self):
        if not os.path.isfile('Q_table.json'):
            Q_learning_training(100000)

        with open('Q_table.json', 'r') as file:
            Q = json.load(file)

    def getMove(self, game):
        state = str(game.board) + str(game.currentPlayer)
        if state in self.Q:
            return max(self.Q[state], key=self.Q[state].get)
        else:
            return np.random.choice(game.onlyPossibleMoves())


if __name__ == "__main__":
    Q_learning_training()
