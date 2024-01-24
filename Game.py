import evaluateFunction


class ConnectFour:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.currentPlayer = 'X'
        self.val1 = 1
        self.val2 = 5
        self.val3 = 100
        self.val4 = 1000

    def printBoard(self):
        for row in self.board:
            print('|'.join(row))

    def isAPossibleMove(self, column):
        if (column > 6 or column < 0):
            return False
        elif (self.board[0][column] != ' '):
            return False
        else:
            return True

    def isCollumnEmpty(self, column):
        if (column > 6 or column < 0):
            return True
        elif (self.board[5][column] == ' '):
            return True
        else:
            return False

    def isBoardFull(self):
        for column in range(7):
            if (self.board[0][column] == ' '):
                return False
        return True

    def isWin(self, column):
        row = 0
        while (self.board[row][column] == ' '):
            row += 1
        # Check vertical grid
        if (row <= 2):
            if (self.board[row][column] == self.board[row+1][column] == self.board[row+2][column] == self.board[row+3][column]):
                return True
        # Check horizontal grid
        for i in range(max(0, column-3), min(3, column)):
            if (self.board[row][i] == self.board[row][i+1] == self.board[row][i+2] == self.board[row][i+3]):
                return True
        # Check diagonal grid
        for i in range(4):
            if (row+i-3 >= 0 and row+i <= 5 and column+i-3 >= 0 and column+i <= 6):
                if (self.board[row+i-3][column+i-3] == self.board[row+i-2][column+i-2] == self.board[row+i-1][column+i-1] == self.board[row+i][column+i]):
                    return True
            if (row-i+3 <= 5 and row-i >= 0 and column+i-3 >= 0 and column+i <= 6):
                if (self.board[row-i+3][column+i-3] == self.board[row-i+2][column+i-2] == self.board[row-i+1][column+i-1] == self.board[row-i][column+i]):
                    return True
        return False

    def makeMove(self, column):
        for row in range(5, -1, -1):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.currentPlayer
                break

    def switchPlayer(self):
        self.currentPlayer = 'O' if self.currentPlayer == 'X' else 'X'

    def copy(self):
        newGame = ConnectFour()
        newGame.board = [row[:] for row in self.board]
        newGame.currentPlayer = self.currentPlayer
        return newGame

    def getRow(self, row):
        return self.board[row]

    def getColumn(self, column):
        return [row[column] for row in self.board]

    def getPossibleMoves(self):
        possibleMoves = []
        for column in range(7):
            if self.isAPossibleMove(column):
                tempGame = self.copy()
                tempGame.makeMove(column)
                possibleMoves.append((tempGame, column))
        return possibleMoves

    def play(self):
        while True:
            self.printBoard()

            if self.isBoardFull():
                print("Draw!")
                break

            column = int(
                input(f"Player {self.currentPlayer}, enter a column (0-6): "))
            if (not self.isAPossibleMove(column)):
                print("Invalid move")
                continue
            self.makeMove(column)
            if self.isWin(column):
                print(f"Player {self.currentPlayer} wins!")
                self.printBoard()
                break
            self.switchPlayer()


# game = ConnectFour()
# game.play()


if __name__ == "__main__":
    game = ConnectFour()
    game.play()
