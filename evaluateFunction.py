


def getDiagonals(game):
    result = []

    for i in range(3):
        for j in range(4):
            diagonal = []
            inverseDiagonal = []
            for k in range(4):
                diagonal.append(game.board[i+k][j+k])
                inverseDiagonal.append(game.board[i+k][6-j-k])
            result.append(diagonal)
            result.append(inverseDiagonal)
    return result


def checkRow(game, row):

    resultX = 0
    resultO = 0
    for i in range(4):
        countX = 0
        countO = 0
        countSpace = 0
        
        for j in range(4):
            if (row[i+j] == 'X'):
                countX += 1
            elif (row[i+j] == 'O'):
                countO += 1
            else:
                countSpace += 1
        if (game.currentPlayer == 'X'):
            if (countX+countSpace == 4 and countSpace != 4):
                match(countX):
                    case 4:
                        resultX += game.val4
                    case 3:
                        resultX += game.val3
                    case 2:
                        resultX += game.val2
                    case 1:
                        resultX += game.val1
            elif (countO + countSpace == 4 and countSpace != 4):
                match(countO):
                    case 4:
                        resultO -= game.val4
                    case 3:
                        resultO -= game.val3
                    case 2:
                        resultO -= game.val2
                    case 1:
                        resultO -= game.val1
        else:
            if (countX+countSpace == 4 and countSpace != 4):
                match(countX):
                    case 4:
                        resultX -= game.val4
                    case 3:
                        resultX -= game.val3
                    case 2:
                        resultX -= game.val2
                    case 1:
                        resultX -= game.val1
            elif (countO + countSpace == 4 and countSpace != 4):
                match(countO):
                    case 4:
                        resultO += game.val4
                    case 3:
                        resultO += game.val3
                    case 2:
                        resultO += game.val2
                    case 1:
                        resultO += game.val1
    return resultX,resultO


def checkColumn(game, column):

    resultX = 0
    resultO = 0
    for i in range(3):
        countX = 0
        countO = 0
        countSpace = 0
        for j in range(4):
            if (column[i+j] == 'X'):
                countX += 1
            elif (column[i+j] == 'O'):
                countO += 1
            else:
                countSpace += 1
        if (game.currentPlayer == 'X'):
            if (countX+countSpace == 4 and countSpace != 4):
                match(countX):
                    case 4:
                        resultX += game.val4
                    case 3:
                        resultX += game.val3
                    case 2:
                        resultX += game.val2
                    case 1:
                        resultX += game.val1
            elif (countO + countSpace == 4 and countSpace != 4):
                match(countO):
                    case 4:
                        resultO -= game.val4
                    case 3:
                        resultO -= game.val3
                    case 2:
                        resultO -= game.val2
                    case 1:
                        resultO -= game.val1
        else:
            if (countX+countSpace == 4 and countSpace != 4):
                match(countX):
                    case 4:
                        resultX -= game.val4
                    case 3:
                        resultX -= game.val3
                    case 2:
                        resultX -= game.val2
                    case 1:
                        resultX -= game.val1
            elif (countO + countSpace == 4 and countSpace != 4):
                match(countO):
                    case 4:
                        resultO += game.val4
                    case 3:
                        resultO += game.val3
                    case 2:
                        resultO += game.val2
                    case 1:
                        resultO += game.val1
    return resultX, resultO


def checkDiagonals(game, diagonals):

    resultX = 0
    resultO = 0 
    for diagonal in diagonals:
        countX = 0
        countO = 0
        countSpace = 0
        for j in range(4):
            if (diagonal[0+j] == 'X'):
                countX += 1
            elif (diagonal[0+j] == 'O'):
                countO += 1
            else:
                countSpace += 1
        if (game.currentPlayer == 'X'):
            if (countX+countSpace == 4 and countSpace != 4):
                match(countX):
                    case 4:
                        resultX += game.val4
                    case 3:
                        resultX += game.val3
                    case 2:
                        resultX += game.val2
                    case 1:
                        resultX += game.val1
            elif (countO + countSpace == 4 and countSpace != 4):
                match(countO):
                    case 4:
                        resultO -= game.val4
                    case 3:
                        resultO -= game.val3
                    case 2:
                        resultO -= game.val2
                    case 1:
                        resultO -= game.val1
        else:
            if (countX+countSpace == 4 and countSpace != 4):
                match(countX):
                    case 4:
                        resultX -= game.val4
                    case 3:
                        resultX -= game.val3
                    case 2:
                        resultX -= game.val2
                    case 1:
                        resultX -= game.val1
            elif (countO + countSpace == 4 and countSpace != 4):
                match(countO):
                    case 4:
                        resultO += game.val4
                    case 3:
                        resultO += game.val3
                    case 2:
                        resultO += game.val2
                    case 1:
                        resultO += game.val1
    return resultX, resultO


def evaluateFunction(game):
    resultX = 0
    resultO = 0
    tempX = 0
    tempO = 0
    for i in range(6):
        tempX , tempO= checkRow(game, game.getRow(i))
        resultX += tempX
        resultO += tempO
       # print(game.getRow(i))
   

    
    for i in range(7):
        tempX, tempO = checkColumn(game, game.getColumn(i))
        resultX+= tempX
        resultO += tempO
    
    diagonals = getDiagonals(game)
    tempX, tempO = checkDiagonals(game, diagonals)
    resultX+= tempX
    resultO += tempO
   
    result = resultX + resultO
    #print(' ')
    return result
