#include <Arduino.h>
#include <Stepper.h>

const int stepsPerRevolution = 200; // change this to match the number of steps per revolution for your motor

Stepper myStepper1(stepsPerRevolution, 14, 27, 26, 25); // initialize the stepper library with the number of steps per revolution and the pin numbers
Stepper myStepper2(stepsPerRevolution, 14, 27, 26, 25);
Stepper myStepper3(stepsPerRevolution, 14, 27, 26, 25);

void setup()
{
    Serial.begin(115200); // initialize serial communication
    myStepper1.setSpeed(60); // set the speed of the motor
    myStepper2.setSpeed(60); 
    myStepper3.setSpeed(60);
}

void loop()
{
    if (Serial.available())
    {
        char received1 = Serial.read();
        if (received1 == 'a')
        {
            Serial.println("Displacing -Y");
            myStepper1.step(-stepsPerRevolution / 4); // rotate the stepper motor by a quarter turn in the counterclockwise direction
        }
        else if (received1 == 'd')
        {
            Serial.println("Displacing Y");
            myStepper1.step(stepsPerRevolution / 4); // rotate the stepper motor by a quarter turn in the clockwise direction
        }
    }

        if (Serial.available())
    {
        char received2 = Serial.read();
        if (received2 == 'z')
        {
            Serial.println("Displacing -X");
            myStepper2.step(-stepsPerRevolution / 4); // rotate the stepper motor by a quarter turn in the counterclockwise direction
        }
        else if (received2 == 'x')
        {
            Serial.println("Displacing X");
            myStepper2.step(stepsPerRevolution / 4); // rotate the stepper motor by a quarter turn in the clockwise direction
        }
    }
}
