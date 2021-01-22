#include <Servo.h>

class Servo_forklift{
  private:
  byte servo_pin;
  int ser_step = 5;
  int center = 85;
  Servo fork_lift;
  
  public:
  Servo_forklift(byte servo)
  {
    servo_pin = servo;
  }

  void Setup()
  {
    fork_lift.attach(servo_pin);
    fork_lift.write(center);
  }

  void down(){
    center = center + ser_step;
    fork_lift.write(center);
    if(center > 165)
    {
      fork_lift.write(165);
    }
  }

  void up()
  {
    center = center - ser_step;
    fork_lift.write(center);
    if(center < 85)
    {
      fork_lift.write(85);
    }
  }
};
