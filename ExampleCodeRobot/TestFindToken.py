import cv2
import numpy as np



def findTokenRed(img1, img2):
    
    b, g, r = cv2.split(img1)
    mask = np.logical_and(g <= r/2, b <= r/2, r >=100)
    img1[mask] = [255, 255, 255]
    mask = np.logical_not(mask)
    img1[mask] = [0, 0, 0]

    b, g, r = cv2.split(img2)
    mask = np.logical_and(g <= r/2, b <= r/2, r>=100)
    img2[mask] = [255, 255, 255]
    mask = np.logical_not(mask)
    img2[mask] = [0, 0, 0]

    img3 = cv2.subtract(img2, img1)

    return img3

def findTokenYellow(img1, img2):
        
    b, g, r = cv2.split(img1)
    mask = np.logical_and(r <= g/2, b <= g/2, g >=100)
    img1[mask] = [255, 255, 255]
    mask = np.logical_not(mask)
    img1[mask] = [0, 0, 0]
    
    b, g, r = cv2.split(img2)
    mask = np.logical_and(r <= g/2, b <= g/2, g>=100)
    img2[mask] = [255, 255, 255]
    mask = np.logical_not(mask)
    img2[mask] = [0, 0, 0]
    
    img3 = cv2.subtract(img2, img1)
    
    return img3

def findBlobInImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 3)
    M = cv2.moments(largest_contour)
    return image,int(M['m10']/M['m00'])

def findCollumWithX(nb , startBoard, endBoard):
    return int((nb-startBoard)/(endBoard-startBoard)*7) 
    
 
    
def findCollum(img1, img2, startBoard, endBoard, color):
    if color == "red":
        img3 = findTokenRed(img1, img2)
    elif color == "yellow":
        img3 = findTokenYellow(img1, img2)
    img3,nb = findBlobInImage(img3)
    col = findCollumWithX(nb, startBoard, endBoard)
    return col, img3
    

if __name__ == "__main__":
    img1 = cv2.imread('ExampleCodeRobot/state1.png')
    img2 = cv2.imread('ExampleCodeRobot/state2.png')
    
    startBoard = 164
    endBoard = 528
    
    col, img3 = findCollum(img1, img2, startBoard, endBoard, "red")
    #col, img4 = findCollum(img1, img2, startBoard, endBoard, "yellow")
    
    print(col)
    
    cv2.imshow('image', img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("done")