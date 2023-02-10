#include <Arduino.h>
#include <Stepper.h>

const int stepsPerRevolution = 200; // change this to match the number of steps per revolution for your motor

Stepper myStepper(stepsPerRevolution, 14, 27, 26, 25); // initialize the stepper library with the number of steps per revolution and the pin numbers

void setup()
{
    Serial.begin(115200); // initialize serial communication
    myStepper.setSpeed(60); // set the speed of the motor
}

void loop()
{
    if (Serial.available())
    {
        char received = Serial.read();
        if (received == 'a')
        {
            Serial.println("Stepper motor rotating counterclockwise");
            myStepper.step(-stepsPerRevolution / 4); // rotate the stepper motor by a quarter turn in the counterclockwise direction
        }
        else if (received == 'd')
        {
            Serial.println("Stepper motor rotating clockwise");
            myStepper.step(stepsPerRevolution / 4); // rotate the stepper motor by a quarter turn in the clockwise direction
        }
    }
}
