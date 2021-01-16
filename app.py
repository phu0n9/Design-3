import json

from flask import request, jsonify
from flask import Flask,render_template, Response

from camera import VideoCamera
from manualControl import *
from threading import Timer

app = Flask(__name__)
app.config["DEBUG"] = True

data = [{}]
trans_data ={
            'velocity':data_display().get('velocity'),
            'power':data_display().get('power'),
            'direction':data_display().get('direction')
        }

def update_data(interval):
    Timer(interval, update_data, [interval]).start()
    global transfer_data
    transfer_data =  {
            'velocity':data_display().get('velocity'),
            'power':data_display().get('power'),
            'direction':data_display().get('direction')
        }
    return transfer_data

@app.route('/home',methods=['GET'])
def show_ui():
    # velocity = data_display().get('velocity')
    # direction = data_display().get('direction')
    # power = data_display().get('power')
    # det_object = "None"
    # , velocity=velocity, direction=direction, power=power, det_object=det_object
    return render_template("index.html") 

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
    return jsonify(data)

@app.route('/transfer',methods=['GET','POST'])
def transfer_data():
    if request.method == 'GET':
        return jsonify(update_data(1000))
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True,threaded=True)

