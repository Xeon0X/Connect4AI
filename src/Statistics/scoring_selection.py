import random as rd
from src.Player import Player
from src.Game import ConnectFour
from src.IAs.alphaBeta import alphaBeta
AI1_WON = 0
AI2_WON = 1
DRAW = 2
NUMBER_OF_AI = 20
NUMBER_AI_SELECTED = 5
DEPTH = 4
NUMBER_OF_GENERATION = 5

def gameLoop(ai1,ai2):
    game = ConnectFour()
    while True:
        if game.isBoardFull():
            return DRAW
        
        if game.currentPlayer == ai1.symbol:
            column = alphaBeta(game, DEPTH, ai1)
        else:
            column = alphaBeta(game, DEPTH , ai2)

        game.makeMove(column)
        if game.isWin(column):
            if(game.currentPlayer == ai1.symbol):
                return AI1_WON
            else:
                return AI2_WON

def compete(ai1,ai2):
    scores = {ai1.symbol:0, ai2.symbol:0, "Draw":0}
    result = (gameLoop(ai1,ai2), gameLoop(ai2,ai1))
    for res in result:
        if res == AI1_WON:
            scores[ai1.symbol] += 1
        elif res == AI2_WON:
            scores[ai2.symbol] += 1
        else:
            scores["Draw"] += 1
    return scores

def generate_population(number):
    return [[rd.randint(1,5),rd.randint(5,15),rd.randint(30,70),1000] for _ in range(number)]

def print_ai(index,population,scores):
    print(index+1,"/",NUMBER_OF_AI,"- score:",scores[index],"-",population[index][:3])

def main():
    population = generate_population(NUMBER_OF_AI)
    for generation in range(NUMBER_OF_GENERATION):
        scores = {i:0 for i in range(NUMBER_OF_AI)}
        for ai1 in range(NUMBER_OF_AI-1):
            for ai2 in range(ai1+1,NUMBER_OF_AI):
                player1 = Player('X',population[ai1])
                player2 = Player('O',population[ai2])
                result = compete(player1,player2)
                scores[ai1] += result[player1.symbol] + result["Draw"]/4
                scores[ai2] += result[player2.symbol] + result["Draw"]/4
            print_ai(ai1,population,scores)
        print_ai(NUMBER_OF_AI-1,population,scores)

        population = sorted(population,key=lambda x: scores[population.index(x)],reverse=True)[:NUMBER_AI_SELECTED]
        population += generate_population(NUMBER_OF_AI-NUMBER_AI_SELECTED)
        print("Generation",generation+1,"ended")
    print(sorted(population,key=lambda x: scores[population.index(x)],reverse=True)[:NUMBER_AI_SELECTED])

if __name__ == "__main__":
    main()