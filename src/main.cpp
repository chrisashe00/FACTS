#include <Arduino.h>
#include <Stepper.h>
#include <Ps3Controller.h>

// change this to the number of steps on your motor
#define STEPS 200

// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to
Stepper stepper(STEPS, 14, 27 ,26, 25);


void setup()
{
  Ps3.begin("01:02:03:04:05:06");
  Serial.println("Ready.");

  Serial.begin(115200);
  Serial.println("Stepper test!");
  // set the speed of the motor to 30 RPMs
  stepper.setSpeed(60);
}

void loop()
{
  if (Ps3.isConnected()){
    Serial.println("Connected!");
  }
  delay(3000);

  if (Serial.available > 0 ){
    const char command == Serial.read();

    if (command == 'h'){}
    
  }
}