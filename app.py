import json
# import serial
# import time
from flask import request, jsonify
from flask import Flask,render_template

# ser = serial.Serial('COM6', 9600, timeout = 1, write_timeout=1)
# from Keyboardcontrol import *

app = Flask(__name__)
app.config["DEBUG"] = True

data = [{}]

@app.route('/home',methods=['GET'])
def show_ui():
    return render_template("index.html") 

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return jsonify(data)
    else:
        req = request.json
        data[0] = req
        print(data[0].get('key'))
        # Keyboard(data[0].get('key'))
        return jsonify(data)
        
# def Keyboard(key):
#     serial.Serial.flush(ser)
#     serial.Serial.flushOutput(ser)
#     if(key == 'w'):
#         ser.write(key.encode())
#     elif (key == 's'):
#         ser.write(key.encode())
#     elif (key == 'a'):
#         ser.write(key.encode())    
#     elif (key == 'd'):
#         ser.write(key.encode())
#     time.sleep(0.05)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

