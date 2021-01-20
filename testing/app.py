import json
import time

from flask import request, jsonify, templating
from flask import Flask,render_template, Response
import threading

from camera import VideoCamera, get_result
from manualControl import *
from threading import Timer
import random
from random import randrange

app = Flask(__name__)
app.config["DEBUG"] = True

data = [{}]

@app.route('/home',methods=['GET'])
def show_ui():
    return render_template("index.html") 

def gen(camera):
    while True:
        frame = camera.get_frame()[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/',methods=['GET'])
def transfer_data():
    power,velocity,direction = data_display()
    trans_data ={
    'velocity':velocity,
    'power':power,
    'direction':direction
    }
    print("trans",trans_data)
    
    data_display()[0].clear()
    data_display()[1].clear()
    data_display()[2].clear()
    return jsonify(trans_data)

@app.route('/stop',methods=['GET'])
def stop():
    flush_data()
    ser.write('r'.encode())
    return jsonify('r')

@app.route('/mode',methods=['GET'])
def change_mode():
    flush_data()
    ser.write('m'.encode())
    return jsonify('m')

# @app.route('/shape',methods=['GET'])
# def get_shape():
#     shape = {"shape":get_result()}
#     return jsonify(shape)

@app.route('/right',methods=['GET'])
def turn_right():
    flush_data()
    ser.write('d'.encode())
    return jsonify('d')

@app.route('/left',methods=['GET'])
def turn_left():
    flush_data()
    ser.write('a'.encode())
    return jsonify('a')

@app.route('/up',methods=['GET'])
def turn_up():
    flush_data()
    ser.write('w'.encode())
    return jsonify('w')

@app.route('/down',methods=['GET'])
def turn_down():
    flush_data()
    ser.write('s'.encode())
    return jsonify('s')

@app.route('/lift_up',methods=['GET'])
def lift_up():
    flush_data()
    ser.write('o'.encode())
    return jsonify('o')

@app.route('/lift_down',methods=['GET'])
def lift_down():
    flush_data()
    ser.write('p'.encode())
    return jsonify('p')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True,threaded=True)
