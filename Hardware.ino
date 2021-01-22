//define library
#include <math.h> 
#include "Motor.h"
#include <SharpIR.h>
#include <NewPing.h>
#include "Forklift.h"
#include <MPU6050_tockn.h>
#include <Wire.h>

#define TRIG_PIN 27 
#define ECHO_PIN 25 
#define MAX_DISTANCE 400 

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE); 
int distance = 100;

//define pin Motor 
#define Ena1 6
#define M1_A 22
#define M1_B 24

//Pins for motor2:
#define Ena2 7
#define M2_A 26
#define M2_B 28

#define servo_pin 9

#define speed_A 72 
#define speed_B 74  

//Motor object 
Motor_Wheel motor_wheel(Ena1,M1_A,M1_B,Ena2,M2_A,M2_B);

//MPU object 
MPU6050 mpu6050(Wire,0.013,0.97);
float compass;

//Servo_forklift object
Servo_forklift servo(servo_pin);

//IRSensor object
SharpIR sensor1( SharpIR::GP2Y0A21YK0F , A0);
SharpIR sensor2( SharpIR::GP2Y0A21YK0F , A1);
SharpIR sensor3( SharpIR::GP2Y0A21YK0F , A2);

typedef enum {start, initial, follow_wall, gap1, turn_left1, obstacle1, turn_left2, obstacle2, object, manual} STATE;
STATE robot_mode = start, prev_state = start;      

int distance1 = 0, distance2 = 0, distance3 = 0, distance4 = 0, count_init = 0, count_stuck = 0, count_track = 0, count = 0, count_gap = 0, count_tl1 = 0, count_tl2 = 0, count_obs = 0;
int d1 = 0, d2 = 0, d3 = 0, d4 = 0, i = 0, j = 0, k = 0, l = 0;

int current_time = 0, previous_time = 0;
int current_time2 = 0, previous_time2 = 0;

volatile long encoderValue = 0;
char input;
double velocity;

void setup()
{
  Serial.begin(9600);
  motor_wheel.Setup();
  
  servo.Setup();
  pinMode(3, INPUT_PULLUP);
  
  digitalWrite(3, HIGH);

  attachInterrupt(digitalPinToInterrupt(3), updateEncoder, HIGH); 
  
  distance = readPing();
  distance1 = read_sensor1(); //body right sensor
  distance2 = read_sensor2(); //tail right sensor
  distance3 = read_sensor3(); //left front senso
  Wire.begin();
  mpu6050.begin();
  mpu6050.setGyroOffsets(-4.16,-0.11,1.03);
  delay(60);

  cli();
  TCCR1A = 0;
  TCCR1B = 0;
  TIMSK1 = 0;

  TCCR1B |= (1 << CS11) | (1 << CS10);
  TCNT1 = 60536;
  TIMSK1 = (1 << TOIE1);

  
  sei();
}

int readPing() { 
  int cm = sonar.ping_cm();
  if(cm==0)
  {
    cm = MAX_DISTANCE;
  }
  return cm;
}

int read_sensor1(){
  int d1 = sensor1.getDistance(); //right front sensor
  if(d1 >= 40 && i < 10)
  {
    i++;
  }
  else if(d1 <40 && i > 1)
  {
    i--;
  }

  if(i >= 10)
  {
    distance1 = 40;
  }
  else if(i <= 1)
  {
    distance1 = d1;
  }
  return distance1;
}

int read_sensor2(){
  int d2 = sensor2.getDistance(); //right front sensor
  if(d2 >= 40 && j < 10)
  {
    j++;
  }
  else if(d2 < 40 && j > 1)
  {
    j--;
  }

  if(j >= 10)
  {
    distance2 = 40;
  }
  else if(j <= 1)
  {
    distance2 = d2;
  }
  return distance2;
}

int read_sensor3(){
  int d3 = sensor3.getDistance(); //right front sensor
  if(d3 >= 60 && k < 10)
  {
    k++;
  }
  else if(d3 < 60 && k > 1)
  {
    k--;
  }

  if(k >= 10)
  {
    distance3 = 60;
  }
  else if(k <= 1)
  {
    distance3 = d3;
  }
  return distance3;
}

float orientation(){
  mpu6050.update();
  compass = mpu6050.getAngleZ();
  
  if(compass < 0)
  {
    compass = compass + 360;
  }
  else if(compass > 360)
  {
    compass = compass - 360;
  }
  return compass;
}

/*Manual control received signal*/
void manual_control(){
  while(Serial.available())
  {
    delay(3);
    input = Serial.read();
  }
  //current_time = millis();
  
  switch(input)
  {
    case 'w': motor_wheel.fwd(100, 100); break;
    case 's': motor_wheel.back(100, 100); break;
    case 'a': motor_wheel.left(100, 100); break;
    case 'd': motor_wheel.right(100, 100); break;
    case 'o': servo.up(); break;
    case 'p': servo.down(); break;
    default: motor_wheel.sto(speed_A, speed_B); break;
  }
  current_time = millis();
  if(input == 'o' || input == 'p'){
    if(current_time - previous_time > 5){
      input = '0';
      previous_time = current_time;
    }
  }
  else{
    if(current_time - previous_time > 100){
      input = '0';
      previous_time = current_time;
    }
  }
}

/*Calculation remaining power capacity of battery*/
float power(){
  int sensorValue = analogRead(A8);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * (5.0 / 1023.0);
  // print out the value you read:
  float power_consumption = voltage*2.85*500;
  return power_consumption; 
}

/*Sending parameter to Raspberry Pi*/
void sending_data(){
    current_time2 = millis();
    if(current_time2 - previous_time2 >= 400){
      Serial.print(power());
      Serial.print(" ");
      Serial.print(velocity);
      Serial.print(" ");
      Serial.print(orientation());
      Serial.print(" ");
      Serial.println(robot_mode);
      previous_time2 = current_time2;
    }
}

void updateEncoder(){
  encoderValue++;
}

/*Timer Interrupt to calculate speed*/
ISR (TIMER1_OVF_vect){
  TCNT1 = 60536;
  velocity = (encoderValue*60*1000)/(20*374);
  //Serial.println(velocity);
  encoderValue = 0;
}

void loop() {
//  Serial.println(read_sensor3());
  switch(robot_mode) {
    /*State 0 Received the signal to start*/
    case start:
     while(Serial.available()){
      delay(3);
      input = Serial.read();
      if(input == 'r'){
        robot_mode = initial;
        break;
      }
     }
    break;    
    /*State 1 Initial start*/                                                       
    case initial:
      delay(3);
      distance1 = read_sensor1();
      distance2 = read_sensor2();
      if((distance1 <= 20) && (distance2 <= 20)) {
        count_init++;
        if(count_init >= 6) {
          count_init = 0;
          prev_state = initial;
          robot_mode = follow_wall;
        }  
      } else motor_wheel.fwd(speed_A, speed_B);
    break;

    /*State 2 Following wall*/
    case follow_wall:
      distance1 = read_sensor1();
      distance2 = read_sensor2();
      if((distance1 <= 30) && (distance2 <= 30)) //sensor 1 and sensor 2 hit a wall
      {
        if(distance1 == 7 && distance2 == 7) distance1 = 6;
        else if(distance1 == 7 && distance1 - distance2 < 0) {
          count_stuck++;
          if(count_stuck >= 5) {
            motor_wheel.left(speed_A, speed_B);
            delay(30);
            count_stuck = 0;
          } 
        }
        float kp = 5.0; 
        int error = distance1 - distance2;
        float correction = kp*error;
        if(error > 8) { // filter out rapid distance 1 increment
           count_track++;
           if(count_track >= 4) {
            motor_wheel.fwd(speed_A, speed_B + correction);
            count_track = 0;
           }
        } else motor_wheel.fwd(speed_A, speed_B + correction);  
      } else if(distance1 > 30) { //sensor 1 starts detecting a gap
        motor_wheel.sto(speed_A, speed_B);
        while(count < 4) { //if the robot is in a gap long enough, change state 
          distance1 = read_sensor1();
          if(distance1 > 30) count++;
        }
        count = 0;
        if(prev_state == initial) robot_mode = gap1;
        else if(prev_state == gap1) robot_mode = turn_left1;
      }
//      Serial.println("follow_wall");
    break;
    
    case gap1:
    distance1 = read_sensor1();
    distance2 = read_sensor2();
    if((distance1 <= 20) && (distance2 <= 20)) {
      motor_wheel.sto(speed_A, speed_B);
      while(count_gap > 2) { //if the robot is in a wall long enough, change state 
        distance1 = read_sensor1();
        distance2 = read_sensor2();
        if((distance1 <= 30) && (distance2 <= 30)) count_gap++;
      }
      prev_state = gap1;
      robot_mode = follow_wall;
      count_gap = 0;
    } else motor_wheel.fwd(speed_A, speed_B); 
//    Serial.println("gap1");
    break;
    
    case turn_left1:  
    distance3 = read_sensor3();
    distance1 = read_sensor1();
    distance2 = read_sensor2();
    
    if(distance3 <= 40) {
      motor_wheel.left(speed_A + 5, speed_B + 5);
      delay(30); 
    } else if((distance1 <= 30) && (distance2 <= 30)) {
        count_tl1++; 
        if(count_tl1 >= 3) { //if the robot is in a wall long enough, change state
          prev_state = turn_left1;
          robot_mode = obstacle1;
          count_tl1 = 0; 
        }  
    } else motor_wheel.fwd(speed_A, speed_B);
//    Serial.println("turn_left1");
    break;

    /*State 5 Checking the Qbot */
    case obstacle1:
    distance = readPing();
    distance1 = read_sensor1();
    distance2 = read_sensor2();
    distance3 = read_sensor3();
    if(distance <= 17 && distance2 <= 30) motor_wheel.sto(speed_A, speed_B);
    else if(distance3 <= 22) motor_wheel.sto(speed_A, speed_B); 
    else if(distance2 > 30 && distance3 > 22) { // turn left once both distance 1 and 3 are clear of sight
        motor_wheel.sto(speed_A, speed_B);
        count_obs++;
        if(count_obs >= 5) {
          prev_state = obstacle1;
          robot_mode = turn_left2;
          count_obs = 0;
        }
    } else if((distance1 <= 30) && (distance2 <= 30)) {
      if(distance1 == 7 && distance2 == 7) distance1 = 6;
        else if(distance1 == 7 && distance1 - distance2 < 0) {
          count_stuck++;
          if(count_stuck >= 3) {
            motor_wheel.left(speed_A + 5, speed_B + 5);
            delay(30);
            count_stuck = 0;
          }
        }
        float kp = 4.0; 
        int error = distance1 - distance2;
        float correction = kp*error;
        if(error > 8) { // filter out rapid distance 1 increment
           count_track++;
           if(count_track >= 4) {
            motor_wheel.fwd(speed_A, speed_B + correction);
            count_track = 0;
           }
        } else motor_wheel.fwd(speed_A, speed_B + correction);
    } else motor_wheel.fwd(speed_A, speed_B);
//    Serial.println("obstacle1");   
    break;

    case turn_left2:
    distance3 = read_sensor3();
    distance1 = read_sensor1();
    distance2 = read_sensor2();
    if(distance3 <= 40) {
        motor_wheel.left(speed_A + 5, speed_B + 5);
        delay(35); 
    } else if((distance1 <= 20) && (distance2 <= 20)) { 
        count_tl2++;
        if(count_tl2 >= 5) { //if the robot is in a wall long enough, change state
          prev_state = turn_left2;
          robot_mode = obstacle2;
          count_tl2 = 0; 
        }
    } else motor_wheel.fwd(speed_A, speed_B);
//    Serial.println("turn_left2");
    break;
    
    case obstacle2:
    distance = readPing();
    distance1 = read_sensor1();
    distance2 = read_sensor2();
    if(distance <= 20 && distance2 <= 30) motor_wheel.sto(speed_A, speed_B);
    else if((distance1 <= 30) && (distance2 <= 30)) //sensor 1 and sensor 2 hit a wall
    {
      if(distance1 == 7 && distance2 == 7) distance1 = 6;
        else if(distance1 == 7 && distance1 - distance2 < 0) {
          count_stuck++;
          if(count_stuck >= 3) {
            motor_wheel.left(speed_A + 5, speed_B + 5);
            delay(30);
            count_stuck = 0;
          }
        }
        float kp = 4.0; 
        int error = distance1 - distance2;
        float correction = kp*error;
        if(error > 8) { // filter out rapid distance 1 increment
           count_track++;
           if(count_track >= 2) {
            motor_wheel.fwd(speed_A, speed_B + correction);
            count_track = 0;
           }
        } else motor_wheel.fwd(speed_A, speed_B + correction);
    }
    else if(distance1 > 30 || distance2 > 30) {
          prev_state = obstacle2;
          motor_wheel.fwd(speed_A + 50, speed_B + 50);
          delay(700);
          robot_mode = object;
    } 
//    Serial.println("obstacle2");
    break;

    /*State 8 Stop before the pallet*/
    case object:
    motor_wheel.sto(speed_A, speed_B);
    while(Serial.available()){
      delay(3);
      input = Serial.read();
      if(input == 'm') robot_mode = manual;
      break;
    }
    break;

    /*State 9 Manual Control */
    case manual:
    manual_control();
    break;
    default: break;
  }
  sending_data();
}
