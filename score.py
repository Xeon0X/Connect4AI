def calculateScore(game, player):
    """
    This function calculates the score of a given game state.
    """
    score = 0
    
    #Get the score of all rows
    for rowIndex in range(6):
        row = game.getRow(rowIndex)
        rowSubsets = [[row[i],row[i+1],row[i+2],row[i+3]] for i in range(4)]
        score += getScoreFromLines(rowSubsets, player)
    
    #Get the score of all column
    for columnIndex in range(7):
        column = game.getColumn(columnIndex)
        columnSubsets = [[column[i],column[i+1],column[i+2],column[i+3]] for i in range(3)]
        score += getScoreFromLines(columnSubsets, player)
    
    #Get the score of all diagonals
    diagonals = game.getDiagonals()
    score += getScoreFromLines(diagonals, player)

    return score

def getScoreFromLines(lines, player):
    """
    This function calculates the score of a given a line in the grid (row, column or diagonal).
    
    "lines" is given in the form of a list of subsets of 4 elements.
    """
    scoreX = 0
    scoreO = 0

    for line in range(len(lines)):
        countX = 0
        countO = 0
        countSpace = 0

        for indexLine in range(4):
            if (lines[line][indexLine] == 'X'):
                countX += 1
            elif (lines[line][indexLine] == 'O'):
                countO += 1
            else:
                countSpace += 1

        if (countX + countSpace == 4 and countSpace != 4):
            scoreX += player.scoreValues[countX-1]

        elif (countO + countSpace == 4 and countSpace != 4):
            scoreO += player.scoreValues[countO-1]
    
    if (player.symbol == 'X'):
        return scoreX - scoreO
    else:
        return scoreO - scoreX