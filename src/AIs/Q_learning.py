import numpy as np
from src.Game import ConnectFour
import json
import os

def mirror_state(state):
    mirrored = ""
    for y in range(6):
        for x in range(7):
            mirrored += state[y * 7 + (6 - x)]
    return mirrored

def get_state(game):
    state = ""
    factor_player = 1 if game.currentPlayer == "X" else 2
    for y in range(6):
        for x in range(7):
            if game.board[y][x] == "X":
                state += str(factor_player)
            elif game.board[y][x] == "O":
                state += str(3 - factor_player)
            else:
                state += "0"
    mirrored = mirror_state(state)
    return min(state, mirrored)

def Q_learning_training(num_game = 1000000):
    Q = {}

    alpha = 0.5
    gamma = 0.95
    epsilon = 0.1

    for i in range(num_game):
        game = ConnectFour()
        state = get_state(game)

        while not game.isBoardFull():
            if np.random.uniform() < epsilon or state not in Q:
                action = np.random.choice(game.onlyPossibleMoves())
            else:
                action = max(Q[state], key=Q[state].get)

            game.makeMove(action)
            next_state = get_state(game)

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

    def get_move(self, game):
        state = get_state(game)
        mirrored_state = mirror_state(state)

        if state in self.Q:
            return max(self.Q[state], key=self.Q[state].get)
        elif mirrored_state in self.Q:
            return 6 - max(self.Q[mirrored_state], key=self.Q[mirrored_state].get)
        else:
            return np.random.choice(game.onlyPossibleMoves())


if __name__ == "__main__":
    Q_learning_training()
