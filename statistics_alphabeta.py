from alphaBeta import alphaBeta
from Game import ConnectFour
from Player import Player
import json
import os
import time

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
    """_summary_

    Args:
        depth (int): _description_
    """
    depth_data = [{"depth": i+1, "nbWin": 0, "nbLoose": 0, "nbDraw":0, "win": [], "loose": [], "draw": []} for i in range(0,depth)]
    for i in range(0,depth):
        print(f"Depth {i} : {depth_data[i]}")    
    def update_depth_data(result, depth1, depth2):
        
        result-=1
        print(f"Result: {result}")
        print(f"Depth IA1: {depth1}")
        print(f"Depth IA2: {depth2}")
       
        if (result == depth1):
            print("IA1 win")
            depth_data[depth1]["win"].append(depth2+1)
            depth_data[depth2]["loose"].append(depth1+1)
            depth_data[depth1]["nbWin"] += 1
            depth_data[depth2]["nbLoose"] += 1
        elif (result == depth2):
            print("IA2 win")
            depth_data[depth1]["loose"].append(depth2+1)
            depth_data[depth2]["win"].append(depth1+1)
            depth_data[depth1]["nbLoose"] += 1
            depth_data[depth2]["nbWin"] += 1
        else:
            print("Draw")
            depth_data[depth1]["draw"].append(depth2+1)
            depth_data[depth2]["draw"].append(depth1+1)
            depth_data[depth1]["nbDraw"] += 1
            depth_data[depth2]["nbDraw"] += 1
        
    timeElapsed = time.time()
    for depth1 in range(depth-1):
        for depth2 in range(depth1+1,depth):
            print(f"---------------------------------")
            print(depth1, depth2)
            
            result = gameLoop(depth1+1, depth2+1)
            update_depth_data(result, depth1, depth2)
            result = gameLoop(depth2+1, depth1+1)
            update_depth_data(result, depth2, depth1)
            
            print(f"Games finished")
    
    print(f"---------------------------------")
    print(f"Finished in {time.time() - timeElapsed} seconds")
    print(f"Saving data...")
    
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
    statAlphaBeta(5)