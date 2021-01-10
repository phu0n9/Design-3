
#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire,0.013,0.97);
float compass; 

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu6050.begin();
  mpu6050.setGyroOffsets(-4.16,-0.11,1.03);
}

void loop() {
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
  if(compass > 45 && compass <= 135)
  {
    Serial.println("West");
  }
  else if(compass > 135 && compass <= 225)
  {
    Serial.println("South");
  }
  else if(compass > 225 && compass <= 315)
  {
    Serial.println("East");
  }
  else
  {
    Serial.println("North");
  }
}
