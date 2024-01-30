def calculateScore(game, player):
    """
    This function calculates the score of a given game state.
    """
    score = 0
    
    #Get the score of all rows
    for rowIndex in range(6):
        row = game.getRow(rowIndex)
        score += getScoreFromLine(game, row, player)
    
    # Get the score of all columns
    for columnIndex in range(7):
        column = game.getColumn(columnIndex)
        score += getScoreFromLine(game, column, player)
    
    # Get the score of all diagonals
    diagonals = game.getDiagonals()
    for diagonal in diagonals:
        score += getScoreFromLine(game, diagonal, player)

    return score

def getScoreFromLine(game, line, player):
    """
    This function calculates the score of a given a line in the grid (row, column or diagonal).
    """
    scoreX = 0
    scoreO = 0
    lineLength = len(line)

    for i in range(lineLength - 3):
        subset = line[i:i+4]
        countX = subset.count('X')
        countO = subset.count('O')
        countSpace = subset.count(' ')

        if countX + countSpace == 4 and countSpace != 4:
            scoreX += game.scoreValues[countX-1]
        elif countO + countSpace == 4 and countSpace != 4:
            scoreO += game.scoreValues[countO-1]

    if player == 'X':
        return scoreX - scoreO
    else:
        return scoreO - scoreX