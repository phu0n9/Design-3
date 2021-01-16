import cv2
import numpy as np
import stack
import math
import os
import time
import statistics
from statistics import mode
import sys

frameWidth = 480
frameHeight = 320
lightLevel = 180


def empty():
    pass


# cv2.namedWindow("Parameters")
# cv2.resizeWindow("Parameters", 640, 240)
# cv2.createTrackbar("Threshold 1", "Parameters", 150, 255, empty)
# cv2.createTrackbar("Threshold 2", "Parameters", 255, 255, empty)
# cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# cap.set(10, lightLevel)
start_time = time.localtime(time.time())[5]
num = []
arr = []


def get_contours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = contours[0]  # --- since there is only one contour in the image
    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
    result = 0
    # epsilon = cv2.arcLength(contours[0], True)
    # approx1 = cv2.approxPolyDP(contours[0], epsilon, True)
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
    center = ((leftmost[0] + rightmost[0]) // 2, (leftmost[1] + rightmost[1]) // 2)
    # new_center = ((topmost[0] + bottommost[0]) // 2, (topmost[1] + bottommost[1]) // 2)

    areaMin = cv2.getTrackbarPos("Area", "Parameters")
    x, y, w, h = cv2.boundingRect(approx)

    M = cv2.moments(cnt)

    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"] + 1e-5)
    cY = int(M["m01"] / M["m00"] + 1e-5)

    # if area > 5000 and 5 <= len(approx) <= 12:
        # n = approx.ravel()
        # i = 0
        # for j in n:
        #     if i % 2 == 0:
        #         new_x = n[i]
        #         new_y = n[i + 1]
        #
        #         # String containing the co-ordinates.
        #         string = str(x) + " " + str(y)
        #         new_str = str(i) + " " + str(i)
        #
        #         cv2.circle(imgContour, (new_x, new_y), 5, (0, 0, 255), -1)

    distance = int(math.sqrt(pow(bottommost[0] - cX, 2) + pow(bottommost[1] - cY, 2)))
    if distance < h:
        cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        # print(len(approx))
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

        if 4 <= len(approx) <= 6:
            cv2.putText(imgContour, "Cubic", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            # print("Cubic")
            result = 1
        elif len(approx) == 7:
            cv2.putText(imgContour, "Cylinder", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            # print("Cylinder")
            result = 2
        else:
            diff_2top = distance_center_topmost - distance_center_top
            diff = abs(diff_2top - distance_center_centerSurf)
            if len(approx) == 8 and diff_2top >= distance_center_centerSurf and diff != 1:
                cv2.putText(imgContour, "Sphere", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                # print("Sphere")
                result = 3
            elif len(approx) == 8 and diff_2top < distance_center_centerSurf and diff != 1:
                cv2.putText(imgContour, "Cylinder", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                    # print("Cylinder")
                result = 2
                # i = i + 1
    return result,area,len(approx)


def process_image(image):
    # Processing images
    # imgContour = image.copy()
    imgContour = image

    imgBlur = cv2.GaussianBlur(image, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    noise_removal = cv2.bilateralFilter(imgGray, 5, 75, 75)
    ret, thresh_image = cv2.threshold(noise_removal, 0, 255, cv2.THRESH_OTSU)

    # threshold1 = cv2.getTrackbarPos("Threshold 1", "Parameters")
    # threshold2 = cv2.getTrackbarPos("Threshold 2", "Parameters")

    threshold1 = 150
    threshold2 = 225

    imgCanny = cv2.Canny(thresh_image, threshold1, threshold2)
    imgCanny = cv2.convertScaleAbs(imgCanny)

    kernel = np.ones((3, 3), np.uint8)
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    area = get_contours(imgDil,imgContour)[1]
    points = get_contours(imgDil,imgContour)[2]
    end_time = time.localtime(time.time())[5]
    imgStack = stack.stackImages(0.8, ([image, imgCanny, imgGray], [thresh_image, imgContour, imgDil]))
    # cv2.imshow("frame", imgStack)
    if area > 5000 and 4 <= points <= 10:
        print("remain",int(end_time - start_time))
        num = get_contours(imgDil, imgContour)[0]
        if int(end_time - start_time) <= 10:
            if isinstance(num,int):
                arr.append(num)
        else:
            return True,arr
            # cap.release()
    # get_contours(imgDil, imgContour)

    return False,arr


# while True:
#     success, img = cap.read()
#     key = cv2.waitKey(1)

#     if not success:
#         # print("failed to grab frame")
#         t = mode(arr)
#         if t == 1:
#             print("Cubic")
#         elif t == 2:
#             print("Cylinder")
#         elif t == 3:
#             print("Sphere")
#         break
#     elif key == ord('q'):
#         break
#     else:
#         # cv2.imshow("Frame", img)
#         num = process_image(img)
#         if isinstance(num,int):
#             arr.append(num)
#         else:
#             print("nothing")
#         # arr.append(0)
#         #     # print("num ",num,"type",type(num))
#         print("arr",arr)






