import json

from flask import request, jsonify
from flask import Flask,render_template, Response

from camera import VideoCamera
# from manualControl import *

app = Flask(__name__)
app.config["DEBUG"] = True

data = [{}]

@app.route('/home',methods=['GET'])
def show_ui():
    velocity = "5"
    direction = "34"
    power = "4.24"
    det_object = "None"
    return render_template("index.html", velocity=velocity, direction=direction, power=power, det_object=det_object) 

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return jsonify(data)
    else:
        req = request.json
        data[0] = req
        print(data[0].get('key'))
        # keyboardControl(data[0].get('key'))
        return jsonify(data)
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

