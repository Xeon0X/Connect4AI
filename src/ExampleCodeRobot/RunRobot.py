from pyniryo import *
from src.AIs.alphaBeta import alphaBeta

from Player import *
from Game import *
from time import *

from pose import *

from src.ExampleCodeRobot.TestFindToken import *



def makeMoveRobot(chosenMove,game,robot):
    """
    This function gides the robot to make a move in the game
    
    chosenMove : int
        The column chosen by the player
    game : ConnectFour
        The game object
    robot : NiryoRobot
        The robot object
    """
    robot.open_gripper(speed=500)

    robot.move_pose(connect4_Move1)

    #robot.move_pose(connect4_Move2)

    robot.move_pose(connect4_Move3)
    robot.move_pose(connect4_Token)
    
    
    robot.close_gripper(speed=500)
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
            
    robot.open_gripper(speed=500)
    robot.move_pose(Observation)
    
    game.makeMove(chosenMove)
    return game




def playRobotWithVision(game,robot):
    """
    This function is used to play connect four with the robot using the vision system
    
    game : ConnectFour
        The game object
    robot : NiryoRobot
        The robot object
    """  
    startBoard = 137
    endBoard = 520    
    IA1 = Player('X')
        
    img_compressed = robot.get_img_compressed()
    previus_img = uncompress_image(img_compressed)
       
    while True:
        game.printBoard()
        if game.currentPlayer == "X":
            chosenMove = alphaBeta(game, 5, IA1)
            print(f"Player {IA1.symbol} played column {chosenMove}")
            game = makeMoveRobot(chosenMove,game,robot) 
            sleep(5)
            i = robot.get_img_compressed()
            previus_img = uncompress_image(i)
        else:
            img_compressed = robot.get_img_compressed()
            img_raw = uncompress_image(img_compressed)
            col, img3 = findCollum(previus_img, img_raw, startBoard, endBoard, "red")
            concat_ims = concat_imgs((previus_img, img_raw, img3))
            #show_img("Images raw & undistorted", concat_ims, wait_ms=30)
            if col!=-1:
                game.makeMove(col)
                sleep(1)
                i = robot.get_img_compressed()
                previus_img = uncompress_image(i)   
            else:
                sleep(2)
        if game.isWin(chosenMove):
            game.switchPlayer()
            print(f"Player {game.currentPlayer} wins!")
            game.printBoard()
            break
        if game.isBoardFull():
            print("Draw!")
            game.printBoard()
            break






def playRobotVsRobot(game,robot):
        """
        This function is used to play connect four with the robot against itself
        
        game : ConnectFour
            The game object
        robot : NiryoRobot
            The robot object
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
            if game.isWin(chosenMove):
                game.switchPlayer()
                print(f"Player {game.currentPlayer} wins!")
                game.printBoard()
                break
            if game.isBoardFull():
                print("Draw!")
                game.printBoard()
                break


def playRobotVsHuman(game,robot):
    """
    This function is used to play connect four with the robot against a human
    
    game : ConnectFour
        The game object
    robot : NiryoRobot
        The robot object
    """

    IA1 = Player('X')
    while True:
        game.printBoard()
        if game.currentPlayer == "X":
            chosenMove = alphaBeta(game, 5, IA1)
            print(f"Player {IA1.symbol} played column {chosenMove}")
            game = makeMoveRobot(chosenMove,game,robot)     
        else:
            chosenMove = int(
            input(f"Player {game.currentPlayer}, enter a column (0-6): "))
            
            if (not game.isAPossibleMove(chosenMove)):
                print("Invalid move")
                continue
            else :
                game.makeMove(chosenMove)

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
    
    robot.move_pose(Observation)

    playRobotWithVision(game,robot)

    robot.close_connection()

