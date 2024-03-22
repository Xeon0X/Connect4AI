from pyniryo import *
from alphaBeta import alphaBeta

from Player import *
from Game import *
from time import *

from pose import *



def makeMoveRobot(chosenMove,game,robot):
    robot.push_air_vacuum_pump()

    robot.move_pose(connect4_Move1)

    robot.move_pose(connect4_Move2)

    robot.move_pose(connect4_Move3)
    robot.move_pose(connect4_Token)
    
    
    robot.pull_air_vacuum_pump()
    robot.move_pose(connect4_Move3)
    robot.move_pose(connect4_Move4)
    
    
    
    
    match (chosenMove):
        case 0 :
            robot.move_pose(connect4_Column1)
        case 1 :
            robot.move_pose(connect4_Column2)
        case 2 :
            robot.move_pose(connect4_Column3)
        case 3 :
            robot.move_pose(connect4_Column4)
        case 4:
            robot.move_pose(connect4_Column5)
        case 5 :
            robot.move_pose(connect4_Column6)
        case 6 :
            robot.move_pose(connect4_Column7)
            
    robot.push_air_vacuum_pump()
    robot.move_pose(connect4_AboveGame)
    
    game.makeMove(chosenMove)
    return game




def playRobot(game,robot):
        """
        This function is an example of how to use the ConnectFour class.
        """
        
        
        IA1 = Player('X')
        IA2 = Player('O')
        while True:
            game.printBoard()
            if game.currentPlayer == "X":
                chosenMove = alphaBeta(game, 5, IA1)
                print(f"Player {IA1.symbol} played column {chosenMove}")
                game = makeMoveRobot(chosenMove,game,robot)
            else:
                chosenMove = alphaBeta(game, 5, IA2)
                print(f"Player {IA2.symbol} played column {chosenMove}")
                game = makeMoveRobot(chosenMove,game,robot)
                #chosenMove = int(
                #input(f"Player {game.currentPlayer}, enter a column (0-6): "))
            
                #if (not game.isAPossibleMove(chosenMove)):
               #     print("Invalid move")
                #    continue
                #else :
                 #   game.makeMove(chosenMove)

            if game.isWin(chosenMove):
                game.switchPlayer()
                print(f"Player {game.currentPlayer} wins!")
                game.printBoard()
                break

            if game.isBoardFull():
                print("Draw!")
                game.printBoard()
                break











if __name__ == "__main__":
    
    game = ConnectFour()

    robot = NiryoRobot("10.10.10.10")
    
    robot.update_tool()

    robot.calibrate_auto()
    
    robot.move_pose(connect4_AboveGame)

    playRobot(game,robot)

    robot.close_connection()

