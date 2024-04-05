from alphaBeta import alphaBeta
from Game import ConnectFour
from Player import Player
import json
import time
import sys

def gameLoop(depth1: int, depth2: int):
    game = ConnectFour()
    IA1 = Player('X')
    IA2 = Player('O')
    while True:
        if game.isBoardFull():
            return 0
        
        if game.currentPlayer == IA1.symbol:
            column = alphaBeta(game, depth1, IA1)
        else:
            column = alphaBeta(game, depth2 , IA2)
            
        game.makeMove(column)
        if game.isWin(column):
            if(game.currentPlayer == IA1.symbol):
                return depth1
            else:
                return depth2

def statAlphaBeta(depth: int):
    """Fight 2 AlphaBeta IA with different depth [1,depth] and stock the result of the game.
    The depth is not the same between IAs (You can't have depth 5 vs depth 5).
    Each IA fight two times the other IA: One IA play first then in the second game, he play last 

    Args:
        depth (int): The depth max to analyse
    """
    depth_data = [{"depth": i+1, "nbWin": 0, "nbLoose": 0, "nbDraw":0, "win": [], "loose": [], "draw": []} for i in range(0,depth)]
  
    def update_depth_data(result, depth1, depth2):
        
        result-=1
        if (result == depth1):
            depth_data[depth1]["win"].append(depth2+1)
            depth_data[depth2]["loose"].append(depth1+1)
            depth_data[depth1]["nbWin"] += 1
            depth_data[depth2]["nbLoose"] += 1
        elif (result == depth2):
            depth_data[depth1]["loose"].append(depth2+1)
            depth_data[depth2]["win"].append(depth1+1)
            depth_data[depth1]["nbLoose"] += 1
            depth_data[depth2]["nbWin"] += 1
        else:
            depth_data[depth1]["draw"].append(depth2+1)
            depth_data[depth2]["draw"].append(depth1+1)
            depth_data[depth1]["nbDraw"] += 1
            depth_data[depth2]["nbDraw"] += 1
        
    timeElapsed = time.time()
    total_iterations = depth * (depth - 1) // 2
    completed_iterations = 0
    
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('#'*int(0), int(0)))
    sys.stdout.flush()
    
    for depth1 in range(depth-1):
            for depth2 in range(depth1+1, depth):
                result = gameLoop(depth1+1, depth2+1)
                update_depth_data(result, depth1, depth2)
                result = gameLoop(depth2+1, depth1+1)
                update_depth_data(result, depth2, depth1)

                completed_iterations += 1
                progress = completed_iterations / total_iterations
                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%%" % ('#'*int(20*progress), int(100*progress)))
                sys.stdout.flush()

    print(f"\nFinished in {time.time() - timeElapsed} seconds")
    print("Saving data...")
    
    data = {}
    data["alphaBeta"] = {
        "timeElapsed": time.time() - timeElapsed,
        "depthMax": depth,
        "depthData": depth_data,
    }
    
    with open('dataAlphaBeta.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    print("Done!")

if __name__ == "__main__":
    statAlphaBeta(10)