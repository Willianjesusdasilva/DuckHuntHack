import cv2
import numpy as np
import imutils


image = cv2.imread('pato.jpg')
cv2.imshow('',image)
cv2.waitKey()

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('',image_gray)
cv2.waitKey()

ret, thresh = cv2.threshold(image_gray, 120, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('',thresh)
cv2.waitKey()

eroded = cv2.erode(thresh, np.ones((10, 10)))
cv2.imshow('',eroded)
cv2.waitKey()

dilated = cv2.dilate(eroded, np.ones((20, 20)))
cv2.imshow('',dilated)
cv2.waitKey()

locates = [[(0,370),(18,400)],[(133,290),(185,395)],[(301,337),(431,400)],[(544,368),(588,405)]]
for locate in locates:
    filtered = cv2.rectangle(dilated, locate[0], locate[1], (0, 0, 0), -1)
    cv2.imshow('',filtered)
    cv2.waitKey()

contour = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

black_template = np.zeros(image.shape)
cv2.imshow('',cv2.drawContours(black_template, contour[0], -1, (0, 255, 0), 2))
cv2.waitKey()

contour = imutils.grab_contours(contour)

for c in contour:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

cv2.imshow('',image)
cv2.waitKey()