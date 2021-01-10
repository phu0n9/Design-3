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
import requests

bp = Blueprint("blog", __name__)
#rpi_ip="http://192.168.0.110"

@bp.route("/", methods=("GET", "POST"))
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
        #code that sends a control signal to the robot goes here, e.g. TCP, UDP, HTTP, Bluetooth, etc. Create similar sections for other control methods.
        return ('', 204)
        
        

        

