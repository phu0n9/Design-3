from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from sense_hat import SenseHat
import time

bp = Blueprint("blog", __name__)
sense = SenseHat()
sense.set_imu_config(True, True, True)  # gyroscope accel and compass enable


@bp.route("/getsensors", methods=("GET", "POST"))
def getsensors():
    if request.method == "GET":
        direction = sense.get_compass()
        return (direction)
        

@bp.route("/forward", methods=("GET", "POST"))
def forward():
    """go forward 1 second"""
    if request.method == "GET":
        # some command to go forward goes here
        time.sleep(1)
        # some command to stop goes here
        return
        
@bp.route("/back", methods=("GET", "POST"))
def back():
    """go back 1 second"""
    if request.method == "GET":
        # some command to go forward goes here
        time.sleep(1)
        # some command to stop goes here
        return        

        

