class Motor_Wheel {
  private:
  //pins for motor 1;
  byte EnA;
  byte M_A1;
  byte M_A2;

  //pins for motor 2;
  byte EnB;
  byte M_B1;
  byte M_B2;

  float pwm_1 = 0;
  float pwm_2 = 0;

  public:
  Motor_Wheel(byte Ena_A, byte A_1_pin, byte A_2_pin, byte Ena_B, byte B_1_pin, byte B_2_pin)
  {
    EnA = Ena_A;
    M_A1 = A_1_pin;
    M_A2 = A_2_pin;
    EnB = Ena_B;
    M_B1 = B_1_pin;
    M_B2 = B_2_pin;
  }


  void Setup()
  {
    pinMode(EnA, OUTPUT);
    pinMode(M_A1,OUTPUT);
    pinMode(M_A2,OUTPUT);
    pinMode(EnB, OUTPUT);
    pinMode(M_B1,OUTPUT);
    pinMode(M_B2,OUTPUT); 
  }

 void set_speed(float motor_A, float motor_B){
    pwm_1 = motor_A;
    pwm_2 = motor_B;
    analogWrite(EnA,pwm_1);
    analogWrite(EnB,pwm_2);
 }
 void back(float pwm_A, float pwm_B){
    set_speed(pwm_A, pwm_B);
    digitalWrite(M_A1,HIGH);
    digitalWrite(M_A2,LOW);
    digitalWrite(M_B1,HIGH);
    digitalWrite(M_B2,LOW);
}

 void left(float pwm_A, float pwm_B){
    set_speed(pwm_A, pwm_B);
    digitalWrite(M_A1,LOW);
    digitalWrite(M_A2,HIGH);
    digitalWrite(M_B1,HIGH);
    digitalWrite(M_B2,LOW);
}

 void right(float pwm_A, float pwm_B){
    set_speed(pwm_A, pwm_B);
    digitalWrite(M_A1,HIGH);
    digitalWrite(M_A2,LOW);
    digitalWrite(M_B1,LOW);
    digitalWrite(M_B2,HIGH);
}

 void fwd(float pwm_A, float pwm_B){
    set_speed(pwm_A, pwm_B);
    digitalWrite(M_A1,LOW);
    digitalWrite(M_A2,HIGH);
    digitalWrite(M_B1,LOW);
    digitalWrite(M_B2,HIGH);
}

 void sto(float pwm_A, float pwm_B){
    set_speed(pwm_A, pwm_B);
    digitalWrite(M_A1,LOW);
    digitalWrite(M_A2,LOW);
    digitalWrite(M_B1,LOW);
    digitalWrite(M_B2,LOW);
}
};
