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
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Q_table.json')

    print("Training Q-learning AI...")

    for i in range(1, num_game+1):
        if i % 10000 == 0:
            print(f"Training game {i//1000}k/{num_game//1000}k")

        game = ConnectFour()
        state = get_state(game)
        mirrored_state = mirror_state(state)

        while not game.isBoardFull():
            if state in Q:
                action = int(max(Q[state], key=Q[state].get))
            elif mirrored_state in Q:
                action = 6 - int(max(Q[mirrored_state], key=Q[mirrored_state].get))
            else:
                action = np.random.choice(game.onlyPossibleMoves())

            game.makeMove(action)
            next_state = get_state(game)
            mirrored_next_state = mirror_state(next_state)

            if game.isWin(action):
                if state not in Q:
                    Q[state] = {}
                if action not in Q[state]:
                    Q[state][action] = 0
                Q[state][action] = 1
                break
            if state in Q:
                if action not in Q[state]:
                    Q[state][action] = 0
                Q[state][action] = Q[state][action] + alpha * (gamma * int(max(Q[next_state].values()) - Q[state][action]))
            elif mirrored_state in Q:
                if 6 - action not in Q[mirrored_state]:
                    Q[mirrored_state][6 - action] = 0
                Q[mirrored_state][6 - action] = Q[mirrored_state][6 - action] + alpha * (gamma * int(max(Q[mirrored_next_state].values()) - Q[mirrored_state][6 - action]))
            else:
                Q[state] = {}
                Q[state][action] = 0
            state = next_state
            mirrored_state = mirrored_next_state

    print("Training finished!")
    with open(file_path, 'w') as file:
        json.dump({str(k): {str(i): j for i, j in v.items()} for k, v in Q.items()}, file)
    print("Q-table saved!")

class QLearning:
    def __init__(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Q_table.json')
        if not os.path.isfile(file_path):
            print("Q-table not found, training...")
            Q_learning_training(10000)
        with open(file_path, 'r') as file:
            self.Q = json.load(file)

    def get_move(self, game):
        state = get_state(game)
        mirrored_state = mirror_state(state)

        if state in self.Q:
            return int(max(self.Q[state], key=self.Q[state].get))
        elif mirrored_state in self.Q:
            return 6 - int(max(self.Q[mirrored_state], key=self.Q[mirrored_state].get))
        else:
            print("State not found in Q-table")
            return np.random.choice(game.onlyPossibleMoves())


if __name__ == "__main__":
    Q_learning_training()
