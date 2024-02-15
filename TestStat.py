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
    
    return nbWin,profondeur, time.time() - timeElapsed


def TestStatMinMax(nbIteration):
    nbWin = {"X": 0, "O": 0, "Draw": 0}
    profondeur={"1" :0 , "2" :0 , "3" :0 , "4" :0 , "5" :0 , "6" :0 , "7" :0 }
    timeElapsed = time.time()
    IA1 = Player('X')
    IA2 = Player('O')
    for i in range(nbIteration):
        randomProfondeurIA1 = random.randint(1, 5)
        randomProfondeurIA2 = random.randint(1, 5)
        game = ConnectFour()
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
    
    return nbWin,profondeur, time.time() - timeElapsed


if __name__ == "__main__":
    nbWin,profondeur, timeElapsed = TestStatAlphaBeta(10)
    with open('TestStatAlphaBeta.txt', 'w') as file:
        file.write(f"AlphaBeta\n")
        file.write(f"NbWin: {nbWin}\n")
        file.write(f"Profondeur: {profondeur}\n")
        file.write(f"TimeElapsed: {timeElapsed}\n")
        file.write(f"---------------------\n")
        
    nbWin,profondeur, timeElapsed = TestStatMinMax(10)
    with open('TestStatMinMax.txt', 'w') as file:
        file.write(f"MinMax\n")
        file.write(f"NbWin: {nbWin}\n")
        file.write(f"Profondeur: {profondeur}\n")
        file.write(f"TimeElapsed: {timeElapsed}\n")
        file.write(f"---------------------\n")