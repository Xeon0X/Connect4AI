from enum import Enum
import cv2
import numpy as np

class ColorHSV(Enum):
    """
    MIN HSV, MAX HSV, Invert Hue (bool)
    """
    BLUE = [90, 50, 85], [125, 255, 255], False
    RED = [15, 80, 75], [170, 255, 255], True
    GREEN = [40, 60, 75], [85, 255, 255], False
    ANY = [0, 50, 100], [179, 255, 255], False


def threshold_hsv(img, list_min_hsv, list_max_hsv, reverse_hue=False, use_s_prime=False):
    """
    Take BGR image (OpenCV imread result) and return thresholded image
    according to values on HSV (Hue, Saturation, Value)
    Pixel will worth 1 if a pixel has a value between min_v and max_v for all channels

    :param img: image BGR if rgb_space = False
    :type img: numpy.array
    :param list_min_hsv: list corresponding to [min_value_H,min_value_S,min_value_V]
    :type list_min_hsv: list[int]
    :param list_max_hsv: list corresponding to [max_value_H,max_value_S,max_value_V]
    :type list_max_hsv: list[int]
    :param use_s_prime: True if you want to use S channel as S' = S x V else classic
    :type use_s_prime: bool
    :param reverse_hue: Useful for Red color cause it is at both extremum
    :type reverse_hue: bool
    :return: threshold image
    :rtype: numpy.array
    """
    frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if use_s_prime:
        frame_hsv[:, :, 1] = (1. / 255) * frame_hsv[:, :, 1] * frame_hsv[:, :, 2].astype(np.uint8)

    if not reverse_hue:
        return cv2.inRange(frame_hsv, tuple(list_min_hsv), tuple(list_max_hsv))
    else:
        list_min_v_c = list(list_min_hsv)
        list_max_v_c = list(list_max_hsv)
        lower_bound_red, higher_bound_red = sorted([list_min_v_c[0], list_max_v_c[0]])
        list_min_v_c[0], list_max_v_c[0] = 0, lower_bound_red
        low_red_im = cv2.inRange(frame_hsv, tuple(list_min_v_c), tuple(list_max_v_c))
        list_min_v_c[0], list_max_v_c[0] = higher_bound_red, 179
        high_red_im = cv2.inRange(frame_hsv, tuple(list_min_v_c), tuple(list_max_v_c))
        return cv2.addWeighted(low_red_im, 1.0, high_red_im, 1.0, 0)


def findTokenRed(img1,img2):
    img1 = threshold_hsv(img1, *ColorHSV.RED.value)
    img2 = threshold_hsv(img2, *ColorHSV.RED.value)
    img3 = cv2.subtract(img2, img1)
    return img3
    

def findTokenYellow(img1, img2):
    img1 = threshold_hsv(img1, *ColorHSV.ANY.value)
    img2 = threshold_hsv(img2, *ColorHSV.ANY.value)
    img3 = cv2.subtract(img2, img1)
    return img3

def findBlobInImage(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    blur = cv2.GaussianBlur(gray, (15, 15), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if(M['m00'] !=0):
            return image,int(M['m10']/M['m00'])
    else:
        print("No contours found")   
        return image, 0
   

def findCollumWithX(nb , startBoard, endBoard):
    for i in range (7):
        if(startBoard+i*(endBoard-startBoard)/7 < nb and nb < startBoard+(i+1)*(endBoard-startBoard)/7):
            return 6-i
    return -1
    
 
    
def findCollum(img1, img2, startBoard, endBoard, color):
    if color == "red":
        img3 = findTokenRed(img1, img2)
    elif color == "yellow":
        img3 = findTokenYellow(img1, img2)
    img3, nb = findBlobInImage(img3)
    if nb == 0:
        print("Token not found")
        return -1, img3
    col = findCollumWithX(nb, startBoard, endBoard)
    return col, img3

if __name__ == "__main__":
    img1 = cv2.imread('ExampleCodeRobot/state1.png')
    img2 = cv2.imread('ExampleCodeRobot/state2.png')
    
    startBoard = 137
    endBoard = 520
    
    col, img3 = findCollum(img1, img2, startBoard, endBoard, "red")
    #col, img4 = findCollum(img1, img2, startBoard, endBoard, "yellow")
    
    print(col)
    
    cv2.imshow('image', img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("done")