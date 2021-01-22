from openCV import get_start_time
import cv2
from statistics import mode
import time
from openCV import *
from manualControl import *
arr = []
frameWidth = 480
frameHeight = 320
lightLevel = 130
result = ""

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.video.set(3, frameWidth)
        self.video.set(4, frameHeight)
        self.video.set(10, lightLevel)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.  
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global result
        success, image = self.video.read()

        try:
            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.

            # result, objectInfo = getObjects(image,0.45,0.2)
            # print(objectInfo)

            image = cv2.resize(image,(500,400))
            if not success:
                print("failed to grab frame")
            else:
                print("stage",get_stage())
                if get_stage() == 8:
                    start_time = get_start_time()
                    end_time = time.process_time() - start_time
                    if int(end_time - start_time) < 9:
                        num,new_image = process_image(image)
                        if isinstance(num, int):
                            if num != 0:
                                arr.append(num)
                            else:
                                pass
                        ret, jpeg = cv2.imencode('.jpeg', new_image)
                        return jpeg.tobytes()
                    elif int(end_time - start_time) >= 9:
                        t = mode(arr)
                        if t == 1:
                            result = "Cubic"
                        elif t == 2:
                            result = "Cylinder"
                        elif t == 3:
                            result = "Sphere"
                        ret, jpeg = cv2.imencode('.jpeg', image)
                        return jpeg.tobytes()
        except TypeError:
            print("Data type is error")
        except Exception as e:
            if not image:      # always check for None
                raise ValueError("unable to load Image")

        ret, jpeg = cv2.imencode('.jpeg', image)
        return jpeg.tobytes()

def get_result():
    return result