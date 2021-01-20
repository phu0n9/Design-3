import cv2
import time

from flask.globals import request

from openCV import *
frameWidth = 480
frameHeight = 320
lightLevel = 130
start_time = time.process_time()
result = ""
arr = []

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
        success, image = self.video.read()
        # img = image.copy()
        # end_time = 0
        result = ""
        if not success:
            print("failed to grab frame")
        elif image is None:
            print("image not found")
        # try:
            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.
        # if filtering_data(image) == True:
        #     ret, jpeg = cv2.imencode('.jpeg',image)
        #     return jpeg.tobytes()
        # else:
        result,image = process_image(image)
        ret, jpeg = cv2.imencode('.jpeg',image)
        return jpeg.tobytes()

    
def get_result():
    if VideoCamera.get_frame(VideoCamera())[1] != "":
        return VideoCamera.get_frame(VideoCamera())[1]