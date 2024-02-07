from aigames.games.tictactoe import GameTicTacToe
from games.connect4 import GameConnect4
from core.player import Player
from robot import ned
from robot import pose
from core.parameters import Parameters
from pyniryo import *
import pyttsx3
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('game', help='give name of the game')
    parser.add_argument('player1', help='set id of player one')
    parser.add_argument('player2', help='set id of player two')
    parser.add_argument('--robot1', help='use Niryo robotic arm for player 1', action="store_true")
    parser.add_argument('--robot2', help='use Niryo robotic arm for player 2', action="store_true")
    args = parser.parse_args()

    # Example : >python main.py connect4 alphabeta-5-2 alphabeta-3-1
    # Example : >python main.py connect4 alphabeta-5-2 mcts-10000

    if args.robot1 and args.robot2:
        args.robot1 = False
        args.robot2 = False

    param = Parameters()

    # Players 0 and 1
    players = [Player(args.player1.lower(), args.robot1), Player(args.player2.lower(), args.robot2)]

    # Initialize robotic arm if required
    isRobot = args.robot1 or args.robot2
    engine = pyttsx3.init()
    image_initial = cv2.imread('media/image_initiale.png')
    image_initial = threshold_hsv(image_initial, *ColorHSV.RED.value)
    robot = None
    if isRobot:
        # Robot initialization
        robot_ip_address = '169.254.200.200'
        robot = NiryoRobot(robot_ip_address)
        robot.calibrate_auto()
        robot.update_tool()
        robot.close_gripper(pose.connect4_GameObservation)
        robot.move_joints(pose.connect4_GameObservation)
        # Get camera parameters
        param.camera_mtx, param.camera_dist = robot.get_camera_intrinsics()
        # Speech to text
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[7].id)

    # Game initialization
    match args.game.lower():
        case 'tictactoe':
            game = GameTicTacToe()
            print(game)
        case 'connect4':
            game = GameConnect4()
            print(game)
        case _:
            print("The game is unknown !")
            sys.exit()
    if isRobot:
        engine.say("Let's start!")
        engine.runAndWait()

    # Play
    while not game.isOver:
        if players[int(-(game.currentPlayer - 1)/2)].type == 'human':
            if isRobot:
                a = ned.nedWhatOpponentPlay(robot, param, image_initial)
            else:
                a = int(input('Which action: '))
        else:
            a = players[int(-(game.currentPlayer - 1)/2)].play(game)
            if players[int(-(game.currentPlayer - 1)/2)].isRobot:
                ned.nedPlayAction(robot, game, a)

        game.playAction(a)
        print(game)
        if not game.isOver:
            game.changePlayer()

    # End of game
    if game.winner == 0:
        print('\nThere is no winner')
        engine.say('Draw!')
        engine.runAndWait()
    else:
        print('\nThe winner is', players[int(-(game.currentPlayer - 1)/2)].text)

#     engine.say("I won, stupid human!")
#     robot.move_pose(Pose.Connect4_Win)
#     robot.open_gripper(Pose.Connect4_gripperSpeed)
#     robot.close_gripper(Pose.Connect4_gripperSpeed)
#     engine.runAndWait()

    if isRobot:
        robot.move_pose(pose.connect4_End)
        robot.close_connection()
