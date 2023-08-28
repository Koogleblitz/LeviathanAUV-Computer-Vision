# [+] Libraries that are commented out are only for ROS
#import rospy
#from std_msgs.msg import Float64
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2
import math
import time
import sys

current_yaw = 0
cv_image = 0
YAW_VARIANCE = .017

# [+]- Access the camera, the int parameter determines which camera you are using, may have to change in depending on what computer you run on
video_capture = cv2.VideoCapture(0)
# video_capture = cv2.VideoCapture(1)
# video_capture = cv2.VideoCapture(2)

lower_value_bounds_c1 = np.array([0, 0, 0])
upper_value_bounds_c1 = np.array([255, 255, 75])

houghParam1_c1=40
houghParam2_c1=45
# houghParam1_c1=15
# houghParam2_c1=30

#[+:]-- -------------------------------------------------//
clk= 0
clkRate= 1
clkLim= clkRate*255
#-------------------------------------------------------//

bgrRed= (0, 0, 255)
bgrBlue= (255, 0, 0)
bgrOrange= (100, 100, 255)

kernel_sqr = np.ones((1,1), np.uint8)
kernel_3x1= np.ones((3,1), np.uint8)
kernel_1x3= np.ones((1,3), np.uint8)
blurnel = (2, 2)
while(True):
    ret, img_frame = video_capture.read()
    img_final = img_frame

    # [+:]--- Use this to find the ideal value range, which changes depending on the lighting ---------------------//
    tick= clk//clkRate + 1
    cv2.putText(img_final, "[:+:] CLK: "+ str(tick), org=(10, 20), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=.7, color=(200, 0, 255), thickness=2)
    clk+= 1
    if clk>clkLim: clk=0
    #--------------------------------------------------------------------------------------------------------------//

    #[::+::]======================Debug================|+|+|+|
    clkRate= 1
    upper_value_bounds = np.array([255, 255, 75])
    # [\\+\\]===========================================|-|-|-|

    img_hsv = cv2.cvtColor(img_frame, cv2.COLOR_BGR2HSV)
    img_threshold = cv2.inRange(img_hsv, lower_value_bounds_c1, upper_value_bounds_c1)
    img_dilate = cv2.dilate(img_threshold, kernel_1x3, iterations=4)
    img_erode = cv2.erode(img_dilate, kernel_1x3, iterations=4)
    img_blur = cv2.blur(img_erode, ksize= blurnel)

    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 20,
                  param1=houghParam1_c1,  # edge detection parameter
                  param2=houghParam2_c1,  # accumulator threshold, or how circley the circles need to be to be recognized (higher=more circlely)
                  minRadius=0,
                  maxRadius=100)

    if (type(circles)) is np.ndarray:
        circle_radii = [x[2] for x in circles[0]] 
        circle_indexes = np.argsort(circle_radii)  
        for i in circle_indexes[-2:]: 
            circle = circles[0][i] 
            cv2.circle(img_final, center=(int(circle[0]), int(circle[1])), radius=int(circle[2]+20), color=bgrOrange, thickness=2)  
            text = " -- -- "
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1, 1)  # get the text size
            text_w, text_h = text_size  # get the text width/height
            cv2.putText(img_final, text, org=(int(circle[0])-text_w, int(circle[1])+(text_h//2)+7), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=bgrOrange, thickness=2)
            
    cv2.imshow('2 Circle_1: hsv', img_hsv)
    cv2.imshow('3 Circle_1: threshold', img_threshold)
    cv2.imshow("4 Circle1_: dilated", img_dilate)
    cv2.imshow("5 Circle_1: eroded", img_erode)
    cv2.imshow("6 Circle_1: blur", img_blur)
    cv2.imshow("7 Circle_1: final", img_final)
    cv2.imshow("7 Circle_1: final", img_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()