import json
import time

from flask import request, jsonify
from flask import Flask,render_template, Response
import threading

from camera import VideoCamera, get_result
from manualControl import *

app = Flask(__name__)
app.config["DEBUG"] = True

data = [{}]

# render the html template
@app.route('/home',methods=['GET'])
def show_ui():
    return render_template("index.html") 

# get the camera
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# display the camera into the HTML
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')
    
# get the data from the serial communication and then return it as JSON data file
@app.route('/',methods=['GET'])
def transfer_data():
    data = data_display()
    trans_data = {
        'velocity':data.get('velocity'),
        'power':data.get('power'),
        'direction':data.get('direction'),
    }
    return jsonify(trans_data)

# get API for start
@app.route('/stop',methods=['GET'])
def stop():
    flush_data()
    ser.write('r'.encode())
    return jsonify('r')

# get API for changing mode
@app.route('/mode',methods=['GET'])
def change_mode():
    flush_data()
    ser.write('m'.encode())
    return jsonify('m')

# get API for result of detecting shape
@app.route('/shape',methods=['GET'])
def get_shape():
    shape = {"shape":get_result()}
    return jsonify(shape)

# get API for turning right
@app.route('/right',methods=['GET'])
def turn_right():
    flush_data()
    ser.write('d'.encode())
    return jsonify('d')

# get API for turning left
@app.route('/left',methods=['GET'])
def turn_left():
    flush_data()
    ser.write('a'.encode())
    return jsonify('a')

# get API for going up
@app.route('/up',methods=['GET'])
def turn_up():
    flush_data()
    ser.write('w'.encode())
    return jsonify('w')

# get API for going down
@app.route('/down',methods=['GET'])
def turn_down():
    flush_data()
    ser.write('s'.encode())
    return jsonify('s')

# get API for forklift up
@app.route('/lift_up',methods=['GET'])
def lift_up():
    flush_data()
    ser.write('o'.encode())
    return jsonify('o')

# get API for forklift down
@app.route('/lift_down',methods=['GET'])
def lift_down():
    flush_data()
    ser.write('p'.encode())
    return jsonify('p')

# hosting web by WSGI server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True,threaded=True)
