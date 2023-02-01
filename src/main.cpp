#include <Arduino.h>
#include <Stepper.h>

const int step_360 = 200; // 360 number of steps per/rev
// initialize the stepper library on pins 2-5 n 8-11
Stepper myStepper1(step_360,14,27,26,25);
Stepper myStepper2(step_360,5,18,19,21);

void setup()
{
// set the speed at 60 rpm:
myStepper1.setSpeed(60);//left
myStepper2.setSpeed(60);//right
// initialize the serial port:
Serial.begin(115200);
}
void loop()
{
// step one revolution in one direction:
Serial.println("clockwise");
myStepper1.step(step_360);
delay(500);
}