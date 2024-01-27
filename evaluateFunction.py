def evaluateFunction(game):
    result = 0
    #Get the score of all rows
    for rowN in range(6):
        row = game.getRow(rowN)
        rowElement = [[row[i],row[i+1],row[i+2],row[i+3]] for i in range(4)]
        result += getScore(game, rowElement)
    #Get the score of all column
    for columnN in range(7):
        column = game.getColumn(columnN)
        columnElement = [[column[i],column[i+1],column[i+2],column[i+3]] for i in range(3)]
        result += getScore(game, columnElement)
    #Get the score of all diagonals
    diagonals = game.getDiagonals()
    result += getScore(game, diagonals)

    return result

def getScore(game,arrays):
    result = 0

    for arrayN in range(len(arrays)):
        countX = 0
        countO = 0
        countSpace = 0
        for elementN in range(4):
            if (arrays[arrayN][elementN] == 'X'):
                countX += 1
            elif (arrays[arrayN][elementN] == 'O'):
                countO += 1
            else:
                countSpace += 1
            if(countX + countSpace == 4 and countSpace != 4):
                match(countX):
                    case 4:
                        result += game.val4
                    case 3:
                        result += game.val3 
                    case 2:
                        result += game.val2 
                    case _ :
                        result += game.val1 
            elif(countO + countSpace == 4 and countSpace != 4):
                match(countO):
                    case 4:
                        result -= game.val4 
                    case 3:
                        result -= game.val3 
                    case 2:
                        result -= game.val2 
                    case _ :
                        result -= game.val1 
    
    if(game.currentPlayer == 'X'):
        return - result
    else:
        return result
