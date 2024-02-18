import json
import os
from minmax import minmax
from alphaBeta import alphaBeta
from Game import ConnectFour
import random
import time
from Player import Player

def TestStatAlphaBeta(nbIteration):
    nbWin = {"X": 0, "O": 0, "Draw": 0}
    profondeur={"1" :0 , "2" :0 , "3" :0 , "4" :0 , "5" :0 , "6" :0 , "7" :0 }
    timeElapsed = time.time()
    IA1 = Player('X')
    IA2 = Player('O')
    for i in range(nbIteration):
        randomProfondeurIA1 = random.randint(1, 7)
        randomProfondeurIA2 = random.randint(1, 7)
        game = ConnectFour()
        print(f"Game {i+1} started")
        print(f"Profondeur IA1: {randomProfondeurIA1}")
        print(f"Profondeur IA2: {randomProfondeurIA2}")
        while True:
            if game.isBoardFull():
                nbWin["Draw"] += 1
                break
            if game.currentPlayer == IA1.symbol:
                column = alphaBeta(game, randomProfondeurIA1, IA1)
            else:
                column = alphaBeta(game, randomProfondeurIA2 , IA2)
            if (not game.isAPossibleMove(column)):
                continue
            game.makeMove(column)
            if game.isWin(column):
                if(game.currentPlayer == IA1.symbol):
                    profondeur[str(randomProfondeurIA1)] += 1
                    nbWin[game.currentPlayer] += 1
                else:
                    profondeur[str(randomProfondeurIA2)] += 1
                    nbWin[game.currentPlayer] += 1
                
                break
        print(f"Game {i+1} finished")
    
    data = {}
    
    if os.path.exists('TestStatAlphaBeta.json'):
        with open('TestStatAlphaBeta.json', 'r') as file:
            data = json.load(file)

    if "AlphaBeta" not in data:
        data["AlphaBeta"] = {
            "NbWin": nbWin,
            "Profondeur": profondeur,
            "TimeElapsed": time.time() - timeElapsed,
            "NbIteration": nbIteration
        }
    else:
        data["AlphaBeta"]["NbWin"]["X"] += nbWin["X"]
        data["AlphaBeta"]["NbWin"]["O"] += nbWin["O"]
        data["AlphaBeta"]["NbWin"]["Draw"] += nbWin["Draw"]
        for key in profondeur:
            data["AlphaBeta"]["Profondeur"][key] += profondeur[key]
        data["AlphaBeta"]["TimeElapsed"] += time.time() - timeElapsed
        data["AlphaBeta"]["NbIteration"] += nbIteration

    with open('TestStatAlphaBeta.json', 'w') as file:
        json.dump(data, file, indent=4)


def TestStatMinMax(nbIteration):
    nbWin = {"X": 0, "O": 0, "Draw": 0}
    profondeur={"1" :0 , "2" :0 , "3" :0 , "4" :0 , "5" :0 }
    timeElapsed = time.time()
    IA1 = Player('X')
    IA2 = Player('O')
    for i in range(nbIteration):
        randomProfondeurIA1 = random.randint(1, 5)
        randomProfondeurIA2 = random.randint(1, 5)
        game = ConnectFour()
        print(f"Game {i+1} started")
        print(f"Profondeur IA1: {randomProfondeurIA1}")
        print(f"Profondeur IA2: {randomProfondeurIA2}")
        while True:
            if game.isBoardFull():
                nbWin["Draw"] += 1
                break
            if game.currentPlayer == IA1.symbol:
                column = minmax(game, randomProfondeurIA1, IA1)
            else:
                column = minmax(game, randomProfondeurIA2 , IA2)
            if (not game.isAPossibleMove(column)):
                continue
            game.makeMove(column)
            if game.isWin(column):
                if(game.currentPlayer == IA1.symbol):
                    profondeur[str(randomProfondeurIA1)] += 1
                    nbWin[game.currentPlayer] += 1
                else:
                    profondeur[str(randomProfondeurIA2)] += 1
                    nbWin[game.currentPlayer] += 1
                
                break
        print(f"Game {i+1} finished")
        
    data = {}
    
    if os.path.exists('TestStatMinMax.json'):
        with open('TestStatMinMax.json', 'r') as file:
            data = json.load(file)

    if "AlphaBeta" not in data:
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
    
    TestStatAlphaBeta(100) 
    #TestStatMinMax(3)
   