#include <Arduino.h>
#include <Stepper.h>

<<<<<<< HEAD
/*================PIN DEFINITIONS================*/
#define LEDC_CHANNEL_0  0
#define LEDC_CHANNEL_1  1
#define LEDC_CHANNEL_2  2
#define LEDC_CHANNEL_3  3
=======
const int stepsPerRevolution = 200; // change this to match the number of steps per revolution for your motor
const int stepAngle = 1.8;

Stepper myStepper(stepsPerRevolution, 14, 27, 26, 25); // initialize the stepper library with the number of steps per revolution and the pin numbers
>>>>>>> AccelStepper

int ZPosition = 0; 

float oneFullRev = 4 * stepsPerRevolution * 0.0314 * 2.5;

void setup()
{
    Serial.begin(115200); // initialize serial communication
    myStepper.setSpeed(60); // set the speed of the motor

}

void loop()
{
    if (Serial.available())
    {
        char received1 = Serial.read();
        if (received1 == 'd')
        {
            Serial.println("Displacing -Z");
            
            ZPosition = ZPosition - oneFullRev;
            

            Serial.print("\n");
            Serial.print("Z position:   ");
            Serial.print(ZPosition);
            Serial.println("mm");
            

            myStepper.step(- 4 * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the counterclockwise direction
        }
        else if (received1 == 'u')
        {
            Serial.println("Displacing +Z");

            ZPosition = ZPosition + oneFullRev;


            Serial.print("\n");
            Serial.print("Z Position:  ");
            Serial.print(ZPosition);
            Serial.println("mm");

            myStepper.step(4 * stepsPerRevolution); // rotate the stepper motor by a quarter turn in the clockwise direction
        }

    }

    if (Serial.available() > 0) {
        String input = Serial.readString();
        if (input.equals("r")) {

            ZPosition = 0;

            Serial.println("Z Position set to 0 mm.");
        }
    }
}