
def evaluateFunction(game):
    result = 0
    for i in range(6):
        result += checkRow(game, game.getRow(i))
    for i in range(7):
        result += checkColumn(game, game.getColumn(i))
    diagonals = getDiagonals(game)
    result += checkDiagonals(game, diagonals)
    return result


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

    result = 0
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
        if (countX+countSpace == 4 and countSpace != 4):
            match(countX):
                case 4:
                    result += game.val4
                case 3:
                    result += game.val3
                case 2:
                    result += game.val2
                case _:
                    result += game.val1
        elif (countO + countSpace == 4 and countSpace != 4):
            match(countO):
                case 4:
                    result -= game.val4
                case 3:
                    result -= game.val3
                case 2:
                    result -= game.val2
                case _:
                    result -= game.val1
    return result


def checkColumn(game, column):

    result = 0
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
        if (countX+countSpace == 4 and countSpace != 4):
            match(countX):
                case 4:
                    result += game.val4
                case 3:
                    result += game.val3
                case 2:
                    result += game.val2
                case _:
                    result += game.val1
        elif (countO + countSpace == 4 and countSpace != 4):
            match(countO):
                case 4:
                    result -= game.val4
                case 3:
                    result -= game.val3
                case 2:
                    result -= game.val2
                case _:
                    result -= game.val1
    return result


def checkDiagonals(game, diagonals):

    result = 0
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
        if (countX+countSpace == 4 and countSpace != 4):
            match(countX):
                case 4:
                    result += game.val4
                case 3:
                    result += game.val3
                case 2:
                    result += game.val2
                case _:
                    result += game.val1
        elif (countO + countSpace == 4 and countSpace != 4):
            match(countO):
                case 4:
                    result -= game.val4
                case 3:
                    result -= game.val3
                case 2:
                    result -= game.val2
                case _:
                    result -= game.val1
    return result
