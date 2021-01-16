import cv2

# from objectDetection import *

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.  
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        try:
            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.

            # result, objectInfo = getObjects(image,0.45,0.2)
            # print(objectInfo)
                # cv2.imshow("Output", image)
                # cv2.waitKey(1)
            image = cv2.resize(image,(500,400))

        except Exception as e:
            if not image:      # always check for None
                raise ValueError("unable to load Image")

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
        