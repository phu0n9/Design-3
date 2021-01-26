import cv2
import numpy as np
import stack
import math
import time
from statistics import mode

def empty():
    pass

start_time = time.process_time()

def get_start_time():
    return start_time


def get_contours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    try:
        cnt = contours[0]                   # --- since there is only one contour in the image
        area = cv2.contourArea(cnt)         # contour area
        peri = cv2.arcLength(cnt, True)     
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  
        result = 0

        # find 4 extreme points in contours
        leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
        rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

        # find customized center respectively to the leftmost and the rightmost point
        center = ((leftmost[0] + rightmost[0]) // 2, (leftmost[1] + rightmost[1]) // 2)

        # find contour coordinates, width and height
        x, y, w, h = cv2.boundingRect(approx)

        M = cv2.moments(cnt)

        # calculate x,y coordinate of default center
        cX = int(M["m10"] / M["m00"] + 1e-5)
        cY = int(M["m01"] / M["m00"] + 1e-5)

        # distance between the default center with the bottom point
        distance = int(math.sqrt(pow(bottommost[0] - cX, 2) + pow(bottommost[1] - cY, 2)))

        # only detect if the contours is found (the contours is in the rectangle, this will allow to detect 1 object at a time)
        if distance < h:

            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w - 100, y - 10), cv2.FONT_HERSHEY_COMPLEX,
                        .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w - 100, y - 35), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

            cv2.circle(imgContour, (cX, cY), 5, (0, 0, 255), -1)
            cv2.putText(imgContour, "center", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cv2.line(imgContour, (cX, cY), (bottommost[0], bottommost[1]), (255, 0, 0), thickness=2)
            cv2.line(imgContour, (center[0], center[1]), (bottommost[0], bottommost[1]), (255, 0, 0), thickness=2)

            cv2.circle(imgContour, center, 6, (255, 0, 0), -1)
            cv2.circle(imgContour, bottommost, 6, (255, 0, 0), -1)
            cv2.circle(imgContour, leftmost, 6, (255, 0, 0), -1)
            cv2.circle(imgContour, rightmost, 6, (255, 0, 0), -1)
            cv2.circle(imgContour, topmost, 6, (255, 0, 0), -1)

            distance_center_left = int(math.sqrt(pow(cX - leftmost[0], 2) + pow(cY - leftmost[1], 2)))
            distance_center_right = int(math.sqrt(pow(cX - rightmost[0], 2) + pow(cY - rightmost[1], 2)))
            distance_center_top = int(math.sqrt(pow(cX - topmost[0], 2) + pow(cY - topmost[1], 2)))
            distance_center_bottom = int(math.sqrt(pow(cX - bottommost[0], 2) + pow(cY - bottommost[1], 2)))
            distance_center_centerSurf = int(math.sqrt(pow(cX - center[0], 2) + pow(cY - center[1], 2)))
            distance_center_topmost = int(
                math.sqrt(pow(topmost[0] - center[0], 2) + pow(topmost[1] - center[1], 2)))
            distance_center_leftmost = int(
                math.sqrt(pow(leftmost[0] - center[0], 2) + pow(leftmost[1] - center[1], 2)))
            distance_center_bottomMost = int(
                math.sqrt(pow(bottommost[0] - center[0], 2) + pow(bottommost[1] - center[1], 2)))
            distance_center_rightMost = int(
                math.sqrt(pow(rightmost[0] - center[0], 2) + pow(rightmost[1] - center[1], 2)))

            # draw enclosing circle
            (enclosing_x, enclosing_y), radius = cv2.minEnclosingCircle(cnt)
            center_enclosing = (int(enclosing_x), int(enclosing_y))
            radius = int(radius)
            cv2.circle(imgContour, center_enclosing, radius, (0, 0, 255), 2)
            enclosing_area = math.pi * pow(radius, 2)
            division = enclosing_area / area
            new_division = radius / distance_center_left

            if 4 <= len(approx) <= 6:
                cv2.putText(imgContour, "Cubic", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                result = 1
            elif len(approx) == 7:
                cv2.putText(imgContour, "Cylinder", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                result = 2
            elif len(approx) == 9:
                cv2.putText(imgContour, "Sphere", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                result = 3
            else:
                if len(approx) == 8 and distance_center_bottom > distance_center_bottomMost and new_division >= 1.1:
                    cv2.putText(imgContour, "Sphere", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                                (0, 255, 0), 2)
                    result = 3
                elif len(approx) == 8 and distance_center_bottom <= distance_center_bottomMost and new_division < 1.1:
                    cv2.putText(imgContour, "Cylinder", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                                (0, 255, 0), 2)
                    result = 2
            return result, area, len(approx)
    except IndexError:
        print("Index out of range")


def process_image(image):
    imgHsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Dark Blue color 
    h_min = 90
    h_max = 179
    s_min = 130
    s_max = 255
    v_min = 0
    v_max = 255

    # create mask for color detection
    lower = np.array([h_min, s_min, v_min], np.uint8)
    upper = np.array([h_max, s_max, v_max], np.uint8)
    mask = cv2.inRange(imgHsv, lower, upper)

    # draw black background
    kernel = np.ones((5, 5), np.uint8)

    # dilate black background and the mask
    imgDil = cv2.dilate(mask, kernel)

    # get only the similarity between the real time image and the image with blue color
    imgMask = cv2.bitwise_and(image, imgHsv, mask=mask)

    area = get_contours(imgDil, imgMask)[1]
    points = get_contours(imgDil, imgMask)[2]

    # only execute when the minimum area is 700 and the points are from 4 to 9
    if area > 700 and 4 <= points <= 9: 
        return get_contours(imgDil, imgMask)[0],imgMask
