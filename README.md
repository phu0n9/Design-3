# Engineering Design 3

Name: Group 10
## Hardware implementation

![alt text](https://github.com/phu0n9/Design-3/blob/master/image.png?raw=true)


## Software implementation

### Features:

#### Automatic moving: 
* Following wall
* Turn left
* Obstacle avoidance
* Obstacle detection
* Run through automatic door


#### Manual control:
* Object detection using openCV
* Using keyboard **r** to start the robot
* Using keyboard **m** to switch to manual stage
* Using keyboard **w** to move up
* Using keyboard **a** to turn left
* Using keyboard **d** to turn right
* Using keyboard **s** to move down
* Using keyboard **o** to lift the forklift
* Using keyboard **p** to lift the forklift

#### OpenCV Shape Detection:
**Cubic**
![alt text](https://github.com/phu0n9/Design-3/blob/master/cubic.png?raw=true)&nbsp;

**Cylinder** </br>
![alt text](https://github.com/phu0n9/Design-3/blob/master/cylinder.png?raw=true)



#### To execute the program:

*```Linux terminal```*:
* Jump to the directory of **app.py**
* Type: **sudo python3 app.py**
* Then go to the IP of your raspberry Pi then type in the address of your web browser: **```<Raspberry PI>```/home**

#### Issues:
This project uses **HTTP** as the connection protocol, in which, **REST API** is deployed into the project. However, for the real-time communication, it is not advisable to use this method. For the real-time communication between getting data from the hardware side, **WebSocket** should be considered instead. Moreover, for a smooth and fast signal for the video streaming, **UDP** is more favourable than **WebSocket**. Maybe a hybrid-approach(WebSocket for the real-time data update and UDP for the Video Streaming) would be better.

