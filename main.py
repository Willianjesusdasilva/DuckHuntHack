import numpy as np
import pyautogui
import imutils
import cv2
import mss

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05

def get_duck(image):

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(image_gray, 120, 255, cv2.THRESH_BINARY_INV)

    eroded = cv2.erode(thresh, np.ones((10, 10)))

    dilated = cv2.dilate(eroded, np.ones((20, 20)))
 

    locates = [[(0,370),(18,400)],[(133,290),(185,395)],[(301,337),(431,400)],[(530,300),(588,405)]]
    for locate in locates:
        filtered = cv2.rectangle(dilated, locate[0], locate[1], (0, 0, 0), -1)


    contour = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    black_template = np.zeros(image.shape)

    contour = imutils.grab_contours(contour)

    centers = []

    for c in contour:
        try:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(image, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            centers.append([cX, cY])
        except:
            pass
    
    cv2.imshow('',image)
    cv2.waitKey(10)
    return centers


while True:
    with mss.mss() as sct:
        image = np.array(sct.grab({"top": 336, "left": 195, "width": 708, "height": 484}))
        for cordinate in get_duck(image):  
            pyautogui.click(x=cordinate[0]+195, y=cordinate[1]+336)

