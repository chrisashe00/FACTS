#include <Arduino.h>
#include <Stepper.h>
#include <Ps3Controller.h>

// change this to the number of steps on your motor
#define stepsPerRev 200

const int slpPin = 33;
const int ultPin = 32; 

const int in1 = 14;
const int in3 = 26;
const int in2 = 27;
const int in4 = 25;

Stepper stepx(stepsPerRev, in1,in2,in3,in4);


void setup() {
  Serial.begin(115200);

  stepx.setSpeed(100);

  pinMode(in4 , OUTPUT);
  pinMode(in3 , OUTPUT);
  pinMode(in2 , OUTPUT);
  pinMode(in1 , OUTPUT);

  pinMode(slpPin, OUTPUT);

  digitalWrite(ultPin, HIGH);
  digitalWrite(slpPin, HIGH);

}

void loop() {

  digitalWrite(slpPin, HIGH);

  stepx.step(stepsPerRev);

  Serial.println("stepping");

  delay(1000);

  stepx.step(-stepsPerRev);

  Serial.println("-stepping");

  delay(1000);

  // digitalWrite(slpPin, LOW);

  // delay(1500);


}


