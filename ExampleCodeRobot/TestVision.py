from pyniryo import *

import cv2

observation_pose = PoseObject(
    x=0.184, y=-0.001, z=0.193,
    roll=0.008, pitch=0.383, yaw=-0.02,
)


max_pose1 = PoseObject( x=0.467, y=0.129, z=0.263,
    roll=-0.141, pitch=-0.016, yaw=-0.00,)


max_pose2 = PoseObject( x=0.467, y=-0.129, z=0.263,
    roll=-0.141, pitch=-0.016, yaw=-0.00,)

# Connecting to robot
robot = NiryoRobot("10.10.10.10")
robot.calibrate_auto()

# Getting calibration param
mtx, dist = robot.get_camera_intrinsics()
# Moving to observation pose
robot.move_pose(observation_pose)




while "User do not press Escape neither Q":
    # Getting image
    img_compressed = robot.get_img_compressed()
    # Uncompressing image
    img_raw = uncompress_image(img_compressed)
    # Undistorting
    img_undistort = undistort_image(img_raw, mtx, dist)

    # - Display
    # Concatenating raw image and undistorted image
    concat_ims = concat_imgs((img_raw, img_undistort))

    # Showing images
    key = show_img("Images raw & undistorted", concat_ims, wait_ms=30)
    if key in [27, ord("q")]:  # Will break loop if the user press Escape or Q
        break
    
        

robot.close_connection()