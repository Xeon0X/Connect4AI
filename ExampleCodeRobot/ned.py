from aigames.robot import pose
from pyniryo import *
from skimage.metrics import structural_similarity
import time


def nedPlayAction(robot, game, a):
    if game.name == 'connect4':
        # Catch token
        robot.move_pose(pose.connect4_Move1)
        robot.move_pose(pose.connect4_Move2)
        robot.move_pose(pose.connect4_Move3)
        robot.open_gripper(pose.connect4_gripperSpeed)
        robot.move_pose(pose.connect4_Token)
        robot.close_gripper(pose.connect4_gripperSpeed)
        robot.move_pose(pose.connect4_Move3)
        robot.move_pose(pose.connect4_Move4)
        robot.move_pose(pose.connect4_AboveGame)
        # play
        robot.move_pose(eval('pose.connect4_Column' + str(a+1)))
        robot.open_gripper(pose.connect4_gripperSpeed)
        robot.close_gripper(pose.connect4_gripperSpeed)
        # back to observation pose
        robot.move_pose(pose.connect4_AboveGame)

        robot.move_joints(pose.connect4_GameObservation)


def getImageFromCamera(robot, param):
    # Get image
    image_compressed = robot.get_img_compressed()
    # Uncompress image
    image_distorted = uncompress_image(image_compressed)
    # Undistorted image
    image_undistorted = undistort_image(image_distorted, param.camera_mtx, param.camera_dist)
    return image_undistorted


def transformImage(image):
    image_rouge = threshold_hsv(image, *ColorHSV.RED.value)
    image_transformed = morphological_transformations(image_rouge, morpho_type=MorphoType.CLOSE, kernel_shape=(15, 15),
                                                      kernel_type=KernelType.ELLIPSE)
    return image_transformed


def getPositionOfTokenPlayed(robot, param, imageIni):
    image1_transformed = transformImage(getImageFromCamera(robot, param))
    # show_img("image1", getImageFromCamera(robot, param), wait_ms=30)
    # image2_transformed = transformImage(getImageFromCamera(robot, param))
    # show_img("image2", image2_transformed, wait_ms=30)
    # img_erode = imageIni
    # show_img("difference", img_erode, wait_ms=30)
    #input('')
    score = 1
    while score > 0.998:
        time.sleep(2)
        print(score)
        image2_transformed = transformImage(getImageFromCamera(robot, param))
        difference = cv2.subtract(image2_transformed, image1_transformed)
        img_erode = morphological_transformations(difference, morpho_type=MorphoType.ERODE, kernel_shape=(10, 10),
                                                  kernel_type=KernelType.RECT)
        (score, diff) = structural_similarity(img_erode, imageIni, full=True)
    show_img("image1", getImageFromCamera(robot, param), wait_ms=30)
    image2_transformed = transformImage(getImageFromCamera(robot, param))
    show_img("image2", image2_transformed, wait_ms=30)
    difference = cv2.subtract(image2_transformed, image1_transformed)
    img_erode = morphological_transformations(difference, morpho_type=MorphoType.ERODE, kernel_shape=(10, 10),
                                              kernel_type=KernelType.RECT)
    show_img("difference", img_erode, wait_ms=30)
    # find the position of the new token
    cnt = biggest_contour_finder(img_erode)
    cnt_barycenter = get_contour_barycenter(cnt)
    print(cnt_barycenter)
    return cnt_barycenter
    #return 0


def nedWhatOpponentPlay(robot, param, imageIni):
    (x, y) = getPositionOfTokenPlayed(robot, param, imageIni)
    #y = getPositionOfTokenPlayed(robot, imageIni)
    #x = 0
    if y > 175:
        if x < 168:
            return 6
        elif x < 232:
            return 5
        elif x < 296:
            return 4
        elif x < 359:
            return 3
        elif x < 426:
            return 2
        elif x < 489:
            return 1
        else:
            return 0
    elif y > 87:
        if x < 146:
            return 6
        elif x < 219:
            return 5
        elif x < 290:
            return 4
        elif x < 365:
            return 3
        elif x < 434:
            return 2
        elif x < 507:
            return 1
        else:
            return 0
    else:
        if x < 119:
            return 6
        elif x < 202:
            return 5
        elif x < 286:
            return 4
        elif x < 365:
            return 3
        elif x < 452:
            return 2
        elif x < 535:
            return 1
        else:
            return 0
