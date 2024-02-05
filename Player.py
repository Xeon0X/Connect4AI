class Player:
    def __init__ (self,symbol,scoreValues = [1,5,50,1000]):
        self.symbol = symbol
        self.scoreValues = scoreValues

    def modifyScoreValues(self, scoreValues):
        self.scoreValues = scoreValues