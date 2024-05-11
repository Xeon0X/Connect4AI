import json
import os
from minmax import minmax
from alphaBeta import alphaBeta
from Game import ConnectFour
import random
import time
from Player import Player

X_HAS_WON = 1
O_HAS_WON = 2
DRAW = 0

def TestStatAlphaBeta(nbIteration):
    

    for i in range(nbIteration):
        nbWin = {"X": 0, "O": 0, "Draw": 0}
        profondeur = {"1" :0 , "2" :0 , "3" :0 , "4" :0 , "5" :0 , "6": 0, "7": 0}
        timeElapsed = time.time()
        data = {}
        if os.path.exists('TestStatAlphaBeta.json'):
            with open('TestStatAlphaBeta.json', 'r') as file:
                data = json.load(file)

        randomProfondeurIA1 = random.randint(1, 7)
        randomProfondeurIA2 = random.randint(1, 7)
        print(f"Game {i+1} started")
        print(f"Profondeur IA1: {randomProfondeurIA1}")
        print(f"Profondeur IA2: {randomProfondeurIA2}")
        
        state = gameLoopAlphaBeta(randomProfondeurIA1, randomProfondeurIA2)
        match(state):
            case 1:
                profondeur[str(randomProfondeurIA1)] += 1
                nbWin["X"] += 1
                
            case 2:
                profondeur[str(randomProfondeurIA2)] += 1
                nbWin["O"] += 1
                
            case _ :
                nbWin["Draw"] += 1
                
        print(f"Game {i+1} finished")
        print("-------------------")
        
        if "AlphaBeta" not in data:
            data["AlphaBeta"] = {
                "NbWin": nbWin,
                "Profondeur": profondeur,
                "TimeElapsed": time.time() - timeElapsed,
                "NbIteration": i + 1
            }
        else:
            data["AlphaBeta"]["NbWin"]["X"] += nbWin["X"]
            data["AlphaBeta"]["NbWin"]["O"] += nbWin["O"]
            data["AlphaBeta"]["NbWin"]["Draw"] += nbWin["Draw"]
            for key in profondeur:
                data["AlphaBeta"]["Profondeur"][key] += profondeur[key]
            data["AlphaBeta"]["TimeElapsed"] += time.time() - timeElapsed
            data["AlphaBeta"]["NbIteration"] +=  1

        with open('TestStatAlphaBeta.json', 'w') as file:
            json.dump(data, file, indent=4)
            
        

def gameLoopMinMax(profondeurIA1, profondeurIA2):
    IA1 = Player('X')
    IA2 = Player('O')
    game = ConnectFour()
    while True:
        if game.isBoardFull():
            return DRAW
        
        if game.currentPlayer == IA1.symbol:
            column = minmax(game, profondeurIA1, IA1)
        else:
            column = minmax(game, profondeurIA2 , IA2)
        
        game.makeMove(column)
        if game.isWin(column):
            if(game.currentPlayer == IA1.symbol):
                return X_HAS_WON
            else:
                return O_HAS_WON

def gameLoopAlphaBeta(profondeurIA1, profondeurIA2):
    IA1 = Player('X')
    IA2 = Player('O')
    game = ConnectFour()
    while True:
        if game.isBoardFull():
            return DRAW
        
        if game.currentPlayer == IA1.symbol:
            column = alphaBeta(game, profondeurIA1, IA1)
        else:
            column = alphaBeta(game, profondeurIA2 , IA2)
        
        game.makeMove(column)
        if game.isWin(column):
            if(game.currentPlayer == IA1.symbol):
                return X_HAS_WON
            else:
                return O_HAS_WON
def TestStatMinMax(nbIteration):
    nbWin = {"X": 0, "O": 0, "Draw": 0}
    profondeur = {"1" :0 , "2" :0 , "3" :0 , "4" :0 , "5" :0 }
    timeElapsed = time.time()
    for i in range(nbIteration):
        randomProfondeurIA1 = random.randint(1, 5)
        randomProfondeurIA2 = random.randint(1, 5)
        print(f"Game {i+1} started")
        print(f"Profondeur IA1: {randomProfondeurIA1}")
        print(f"Profondeur IA2: {randomProfondeurIA2}")
        
        state = gameLoopMinMax(randomProfondeurIA1, randomProfondeurIA2)
        match(state):
            case 1:
                profondeur[str(randomProfondeurIA1)] += 1
                nbWin["X"] += 1
                break
            case 2:
                profondeur[str(randomProfondeurIA2)] += 1
                nbWin["O"] += 1
                break
            case _ :
                nbWin["Draw"] += 1
                
        print(f"Game {i+1} finished")
        
        
    data = {}
    
    if os.path.exists('TestStatMinMax.json'):
        with open('TestStatMinMax.json', 'r') as file:
            data = json.load(file)

    if "MinMax" not in data:
        data["MinMax"] = {
            "NbWin": nbWin,
            "Profondeur": profondeur,
            "TimeElapsed": time.time() - timeElapsed,
            "NbIteration": nbIteration
        }
    else:
        data["MinMax"]["NbWin"]["X"] += nbWin["X"]
        data["MinMax"]["NbWin"]["O"] += nbWin["O"]
        data["MinMax"]["NbWin"]["Draw"] += nbWin["Draw"]
        for key in profondeur:
            data["MinMax"]["Profondeur"][key] += profondeur[key]
        data["MinMax"]["TimeElapsed"] += time.time() - timeElapsed
        data["MinMax"]["NbIteration"] += nbIteration

    with open('TestStatMinMax.json', 'w') as file:
        json.dump(data, file, indent=4)


   


if __name__ == "__main__":
    
    TestStatAlphaBeta(10000) 
    #TestStatMinMax(3)
   