import cv2
import numpy as np
import stack
import math
import time
import statistics
from statistics import mode

frameWidth = 480
frameHeight = 320
lightLevel = 130


def empty():
    pass

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# cap.set(10, lightLevel)
arr = []
start_time = time.process_time()


def get_contours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    try:
        cnt = contours[0]  # --- since there is only one contour in the image
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
        result = 0
        # epsilon = cv2.arcLength(contours[0], True)
        # approx1 = cv2.approxPolyDP(contours[0], epsilon, True)

        leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
        rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
        center = ((leftmost[0] + rightmost[0]) // 2, (leftmost[1] + rightmost[1]) // 2)

        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        x, y, w, h = cv2.boundingRect(approx)

        M = cv2.moments(cnt)

        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"] + 1e-5)
        cY = int(M["m01"] / M["m00"] + 1e-5)

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
            distance_center_bottomMost = int(
                math.sqrt(pow(bottommost[0] - center[0], 2) + pow(bottommost[1] - center[1], 2)))
            distance_center_rightMost = int(
                math.sqrt(pow(rightmost[0] - center[0], 2) + pow(rightmost[1] - center[1], 2)))

            (enclosing_x, enclosing_y), radius = cv2.minEnclosingCircle(cnt)
            center_enclosing = (int(enclosing_x), int(enclosing_y))
            radius = int(radius)
            cv2.circle(imgContour, center_enclosing, radius, (0, 0, 255), 2)
            enclosing_area = math.pi * pow(radius, 2)
            division = enclosing_area / area
            new_division = radius / distance_center_left

            # print("radius ", radius)
            # print("new radius", distance_center_left)
            # print("area normal ", area)
            # print("enclosing area ", enclosing_area)
            # # print("distance center ", distance_center_leftmost)
            # print("new division ", new_division)
            # print("division", division)

            if 4 <= len(approx) <= 6:
                cv2.putText(imgContour, "Cubic", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                # print("Cubic")
                result = 1
            elif len(approx) == 7:
                cv2.putText(imgContour, "Cylinder", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                # print("Cylinder", len(approx))
                result = 2
            elif len(approx) == 9:
                cv2.putText(imgContour, "Sphere", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                # print("Cylinder", len(approx))
                result = 2
            else:
                # diff_2top = distance_center_topmost - distance_center_top
                # # diff = abs(diff_2top - distance_center_centerSurf)
                # print("center left", distance_center_left)
                # print("center top", distance_center_top)
                # print("center bottom", distance_center_bottom)
                # print("center right",distance_center_right)
                # print("between center left", distance_center_leftmost)
                # print("between center top", distance_center_topmost)
                # print("between center bottom", distance_center_bottomMost)
                # print("between center right",distance_center_rightMost)
                # diff_2bottom = distance_center_bottomMost - distance_center_bottom
                # diff_2_left = distance_center_leftmost - distance_center_left
                # diff_2_right = distance_center_rightMost - distance_center_right
                # print("2 left ",diff_2_left)
                # print("2 top", diff_2top)
                # print("2 bottom ",diff_2bottom)
                # print("2 right",diff_2_right)
                # diff_top_bottom = diff_2top - diff_2bottom
                # diff_right_left = diff_2_right - diff_2_left
                # print("top and bottom",diff_top_bottom)
                # print("right and left",diff_right_left)
                # diff = abs(diff_top_bottom - diff_right_left)
                # if len(approx) == 7 and distance_center_bottom > distance_center_bottomMost :
                #     cv2.putText(imgContour, "Sphere", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                #                 (0, 255, 0), 2)
                #     print("Sphere",len(approx))
                #     result = 3
                # elif len(approx) == 7 and distance_center_bottom <= distance_center_bottomMost:
                #     cv2.putText(imgContour, "Cylinder", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                #                 (0, 255, 0), 2)
                #     print("Cylinder",len(approx))
                #     result = 2
                if len(approx) == 8 and distance_center_bottom > distance_center_bottomMost and new_division >= 1.1:
                    cv2.putText(imgContour, "Sphere", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                                (0, 255, 0), 2)
                    # print("Sphere", len(approx))
                    result = 3
                elif len(approx) == 8 and distance_center_bottom <= distance_center_bottomMost and new_division < 1.1:
                    cv2.putText(imgContour, "Cylinder", (x + w - 100, y - 55), cv2.FONT_HERSHEY_COMPLEX, .7,
                                (0, 255, 0), 2)
                    # print("Cylinder", len(approx))
                    result = 2
            return result, area, len(approx)
    except IndexError:
        return 0,0,0


def process_image(image):
    # Processing images
    imgContour = image.copy()

    imgHsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Blue ones
    # h_min = 90
    # h_max = 179
    # s_min = 130
    # s_max = 255
    # v_min = 0
    # v_max = 255

    # Orange one
    h_min = 0
    h_max = 179
    s_min = 123
    s_max = 255
    v_min = 130
    v_max = 255

    # Red
    # h_min = 80
    # h_max = 179
    # s_min = 117
    # s_max = 255
    # v_min = 163
    # v_max = 255

    lower = np.array([h_min, s_min, v_min], np.uint8)
    upper = np.array([h_max, s_max, v_max], np.uint8)
    mask = cv2.inRange(imgHsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)

    imgDil = cv2.dilate(mask, kernel)

    area = get_contours(imgDil, imgContour)[1]
    points = get_contours(imgDil, imgContour)[2]
    imgColor = cv2.bitwise_and(image, imgHsv, mask=mask)
    result = get_contours(imgDil, imgContour)[0]

    if area > 500 and 4 <= points <= 9:
        # if isinstance(result, int):
        #     if result != 0:
        #         arr.append(result)
        #         end_time = time.process_time() - start_time
        #         if int(end_time - start_time) > 4:
        #             t = mode(arr)
        #             arr.clear()
        #             if t == 1:
        #                 return "Cubic"
        #             elif t == 2:
        #                 return "Cylinder"
        #             else:
        #                 return "Sphere"
        return result,imgColor
    return 0,image

                