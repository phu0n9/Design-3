from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from werkzeug.exceptions import abort
import time
import socket
from .camera import VideoCamera
from flask import Response
from flask import Flask

PORTNUM = 10001
target = '192.168.0.110'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

bp = Blueprint("blog", __name__)
#rpi_ip="http://192.168.0.110"

data = [{}]

@bp.route("/home", methods=("GET", "POST"))
def index():
    if request.method == "GET":
        #sensors = requests.get(rpi_ip + ":5000/getsensors")
        #sensors=sensors.text
        velocity = "5"
        direction = "34"
        power = "4.24"
        det_object = "None"
        return render_template("blog/index.html", velocity=velocity, direction=direction, power=power, det_object=det_object)
        

@bp.route("/forward", methods=("GET", "POST"))
def forward():
    if request.method == "GET":
        data = bytes('fw','utf-8')
        s.sendto(data, (target, PORTNUM))
        return ('', 204)
        
@bp.route("/back", methods=("GET", "POST"))
def back():
    if request.method == "GET":
        data = bytes('bk','utf-8')
        s.sendto(data, (target, PORTNUM))
        return ('', 204)

@bp.route("/left", methods=("GET", "POST"))
def left():
    if request.method == "GET":
        data = bytes('lt','utf-8')
        s.sendto(data, (target, PORTNUM))
        return ('', 204)

@bp.route("/right", methods=("GET", "POST"))
def right():
    if request.method == "GET":
        data = bytes('rt','utf-8')
        s.sendto(data, (target, PORTNUM))
        return ('', 204)
        
@bp.route("/up", methods=("GET", "POST"))
def up():
    if request.method == "GET":
        data = bytes('up','utf-8')
        s.sendto(data, (target, PORTNUM))
        return ('', 204)
        
@bp.route("/down", methods=("GET", "POST"))
def down():
    if request.method == "GET":
        data = bytes('dn','utf-8')
        s.sendto(data, (target, PORTNUM))
        return ('', 204)
        
@bp.route("/auto", methods=("GET", "POST"))
def auto():
    if request.method == "GET":
        data = bytes('auto','utf-8')
        s.sendto(data, (target, PORTNUM))
        return ('', 204)
        
@bp.route("/manual", methods=("GET", "POST"))
def manual():
    if request.method == "GET":
        data = bytes('manual','utf-8')
        s.sendto(data, (target, PORTNUM))
        return ('', 204)
        

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')

@bp.route("/video_feed", methods=("GET", "POST"))
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/',methods=('GET','POST'))
def home():
	if request.method == 'GET':
		return jsonify(data)
	else:
		print("hello")
		req = request.json
		data[0] = req
		print(data[0].get('key'))
		# keyboardControl(data[0].get('key'))
		return jsonify(data)
