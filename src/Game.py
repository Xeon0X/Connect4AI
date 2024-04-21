class ConnectFour:
    """
    This class represents a game of Connect Four. It contains all the functions needed to play the game.
    """

    def __init__(self):
        """
        Initializes a new ConnectFour object 
        """
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.currentPlayer = 'X'
        self.scoreValues = [1, 5, 50, 1000]

    def printBoard(self):
        """
        Displays the game board in the console
        """
        for row in self.board:
            print('|'.join(row))

    def isAPossibleMove(self, column):
        """Checks if the provided column is a possible move for the player

        Args:
            column (int): The column of the move give by the player

        Returns:
            bool: If the move is possible or not
        """
        if column > 6 or column < 0:
            return False
        elif self.board[0][column] != ' ':
            return False
        else:
            return True

    def isCollumnEmpty(self, column):
        """Checks if the given column is empty

        Args:
            column (int): The column of the move give by the player

        Returns:
            int: If the column is empty or not
        """
        if column > 6 or column < 0:
            return True
        elif self.board[5][column] == ' ':
            return True
        else:
            return False

    def isBoardFull(self):
        """Checks if the board is full

        Returns:
            bool: If the board is full or not
        """
        for column in range(7):
            if self.board[0][column] == ' ':
                return False
        return True

    def isWin(self, column):
        """Checks if the move in the given column is a winning move

        Args:
            column (int): The column of the move give by the player

        Returns:
            bool: If the move is a winning move or not
        """
        row = 0
        while self.board[row][column] == ' ':
            row += 1

        # Check vertical grid
        if row <= 2:
            if self.board[row][column] == self.board[row + 1][column] == self.board[row + 2][column] == self.board[row + 3][column]:
                return True

        # Check horizontal grid
        for i in range(4):
            if (column+i-3 >= 0 and column+i <= 6):
                if (self.board[row][column+i-3] == self.board[row][column+i-2] == self.board[row][column+i-1] == self.board[row][column+i]):
                    return True

        # Check diagonal grid
        for i in range(4):
            if row+i-3 >= 0 and row+i <= 5 and column+i-3 >= 0 and column+i <= 6:
                if self.board[row + i - 3][column + i - 3] == self.board[row + i - 2][column + i - 2] == self.board[row + i - 1][column + i - 1] == self.board[row + i][column + i]:
                    return True

            if row-i+3 <= 5 and row-i >= 0 and column+i-3 >= 0 and column+i <= 6:
                if self.board[row - i + 3][column + i - 3] == self.board[row - i + 2][column + i - 2] == self.board[row - i + 1][column + i - 1] == self.board[row - i][column + i]:
                    return True

        return False

    def makeMove(self, column):
        """
        Makes the move in the given column

        Args:
            column (int): The column of the move give by the player

        Returns:
            int: The row of the move
        """
        for row in range(5, -1, -1):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.currentPlayer
                self.switchPlayer()
                return row

        return -1

    def switchPlayer(self):
        """Changes the current player
        """
        self.currentPlayer = 'O' if self.currentPlayer == 'X' else 'X'

    def copy(self):
        """Copies the current game

        Returns:
            ConnectFour: The copy of the current game
        """
        newGame = ConnectFour()
        newGame.board = [row[:] for row in self.board]
        newGame.currentPlayer = self.currentPlayer
        return newGame

    def getRow(self, row):
        """ Returns the requested row

        Args:
            row (int): The row to return

        Returns:
            list(str): The requested row
        """
        return self.board[row]

    def getColumn(self, column):
        """ Returns the requested column

        Args:
            column (int): The column to return

        Returns:
            list(str): The requested column
        """
        return [row[column] for row in self.board]

    def getDiagonals(self):
        """ Returns all the diagonals of the board

        Returns:
            list(list(str)): All the diagonals of the board
        """
        diagonals = []

        # DIAGONALS UP TO DOWN
        # Diagonals with a length of 4
        diagonals.append([self.board[2+i][i] for i in range(4)])
        diagonals.append([self.board[i][3+i] for i in range(4)])

        # Diagonals with a length of 5
        for n in range(2):
            diagonals.append([self.board[1+i+n][i+n] for i in range(4)])
            diagonals.append([self.board[i+n][2+i+n] for i in range(4)])

        # Diagonals with a length of 6
        for n in range(3):
            diagonals.append([self.board[i+n][i+n] for i in range(4)])
            diagonals.append([self.board[i+n][1+i+n] for i in range(4)])

        # DIAGONALS DOWN TO UP
        # Diagonals with a length of 4
        diagonals.append([self.board[3-i][i] for i in range(4)])
        diagonals.append([self.board[5-i][3+i] for i in range(4)])

        # Diagonals with a length of 5
        for n in range(2):
            diagonals.append([self.board[4-(i+n)][i+n] for i in range(4)])
            diagonals.append([self.board[5-(i+n)][2+i+n] for i in range(4)])

        # Diagonals with a length of 6
        for n in range(3):
            diagonals.append([self.board[5-(i+n)][i+n] for i in range(4)])
            diagonals.append([self.board[5-(i+n)][1+i+n] for i in range(4)])

        return diagonals

    def getPossibleMoves(self):
        """
        This function returns a list of tuples containing all the possible moves and the resulting game state.
        """
        possibleMoves = []
        for column in range(7):
            if self.isAPossibleMove(column):
                gameState = self.copy()
                gameState.makeMove(column)
                possibleMoves.append((gameState, column))
        return possibleMoves

    def onlyPossibleMoves(self):
        """
        This function returns a list containing all the possible moves.
        """
        possibleMoves = []
        for column in range(7):
            if self.isAPossibleMove(column):
                possibleMoves.append(column)
        return possibleMoves

    def checkWin(self):
        """This function checks if a player has won the game.

        Returns:
            bool: If a player has won the game or not
        """
        for column in range(7):
            if not self.isCollumnEmpty(column):
                if self.isWin(column):
                    return True
        return False
      
    def play(self):
        """
        This function is an example of how to use the ConnectFour class.
        """

        while True:
            self.printBoard()

            if self.isBoardFull():
                print("Draw!")
                break

            column = int(
                input(f"Player {self.currentPlayer}, enter a column (0-6): "))
            if not self.isAPossibleMove(column):
                print("Invalid move")
                continue
            self.makeMove(column)
            if self.isWin(column):
                print(f"Player {self.currentPlayer} wins!")
                self.printBoard()
                break
            # self.switchPlayer()


if __name__ == "__main__":
    game = ConnectFour()
    game.play()
